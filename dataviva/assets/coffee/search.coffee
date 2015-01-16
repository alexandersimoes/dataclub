WARNING = "This file was compiled from coffeescript. Do not edit the .js file!"

firstLoad = true

updateSuggestion = false
attr_types = ["bra", "hs", "wld", "cnae", "cbo"]

########## settings ################
threshold = 0.3 # threshold for the fuzzy search
delay     = 100 # delay in ms, so search won't be called as the user is typing
topK      = 15 # show k rows in autosuggest

########## state ###################
lockedAttrs      = [] # an array containing the locked attributes
timeoutID        = null # used to delay the search as the user is typing
attrs            = [] # full, flat attribute list
weights          = {} # weight keys for each attr type, passed with the data
type2fuse        = {}
type2attrs       = {}
type2possibleids = {}
builds           = []
profiles         = []
availBuilds      = []
availTypes       = {}
####################################

dataviva.old_search = (opts) ->

  loading = dataviva.loading(opts.input)
    .text "Loading Attributes"
    .color d3plus.color.text(d3.select(opts.input).style("background-color"))

  loadAttrs opts

loadAttrs = (opts) ->

  q = queue()

  for t in attr_types
    url = "/attrs/" + t + "/?lang=" + dataviva.language
    stored = Modernizr.localstorage and url of localStorage and
           (!(url in dataviva.storage) or
           (parseFloat(localStorage[t]) is dataviva.storage[t]))
    if stored
      data               = JSON.parse localStorage[url]
      dataviva.depths[t] = data.depths
      weights[t]         = data.weight
      type2attrs[t]      = dataviva.cleanData data, t
    else
      q.defer((u, callback) ->
        attr = u.split("/")[2]
        d3.json u, (error, data) ->
          unless error
            localStorage[attr]    = dataviva.storage[attr]
            localStorage[u]       = JSON.stringify data
            dataviva.depths[attr] = data.depths
            weights[attr]         = data.weight
            type2attrs[attr]      = dataviva.cleanData data, attr
          callback error, data
      , url)

  q.awaitAll () ->

    # pre-process attributes (remove accents, assign rank score etc)
    for type, subattrs of type2attrs
      # sort attributes by weight
      weight = weights[type]
      subattrs.sort (a,b) ->
        if b[type+"_id"].length is a[type+"_id"].length
          b[weight] - a[weight]
        else
          b[type+"_id"].length - a[type+"_id"].length
      for attr, i in subattrs
        attr.rank = i
        attr.type = type
        attr.normName = attr.id + " " + dataviva.removeAccents attr.name
        attrs.push attr

      # initialize local fuse for each attribute type
      type2fuse[type] = new Fuse subattrs, {
        keys:         ['normName'],
        includeScore: true,
        threshold:    threshold
      }

    runSearch opts

runSearch = (opts) ->

  lockedBuild = opts.build
  if lockedBuild
    for t, list of lockedBuild.filter_ids
      for a in list
        attr = type2attrs[t].filter (d) -> d[t+"_id"] is a
        lockedAttrs.push(attr[0])

  removeBuild = d3.select(opts.input).html("").append("span")
    .attr "id","removeBuild"
    .on d3plus.client.pointer.click, () ->
      lockedBuild = false
      updateSuggestion()

  searchBox = d3.select(opts.input).append("span")
    .attr "id", "searchItems"

  loadBuild = d3.select(opts.input).append("a")
    .attr "id", "loadBuild"
    .attr "class", "decision arrow inline button"
    .html "Go"

  if opts.profiles
    builder = dataviva.dict.builder
    d3.select(opts.input).append("a")
      .attr "class", "advanced"
      .attr "href", "/builder/"
      .html builder + " <i class='fa fa-angle-double-right'></i>"

  if opts.builds
    buildSuggestions = d3.select(opts.results).append("div")
      .attr "id","buildSuggestions"

  if opts.profiles
    profileSuggestions = d3.select(opts.results).append("div")
      .attr "id","profileSuggestions"
    profileSuggestions.append("h2").text dataviva.dict.profile_plural

  # initialize a global fuse with all the attributes
  fuse = new Fuse attrs, {
    keys:         ['normName'],
    includeScore: true,
    threshold:    threshold
  }

  getIndices = (pattern, str) ->
    startIndex = 0
    searchStrLen = pattern.length
    indices = []
    while  (idx = str.indexOf(pattern, startIndex)) > -1
      indices.push idx
      startIndex = idx + searchStrLen
    return indices

  replaceStart = (orig, pattern, newPattern, start) ->
    orig.substr(0, start) + orig.substr(start).replace(pattern, newPattern)

  removeValue = (array, value) ->
    index = array.indexOf value
    array.splice(index, 1) if index > -1
    return index

  getPossibleIds = (filterType, index, build, cb) ->
    lockedTypes = {}
    lockedTypes[attr.type] = true for attr in lockedAttrs
    if not build? and filterType of lockedTypes
      cb null, null
      return
    if filterType of type2possibleids
      cb null, type2possibleids[filterType]
      return

    dataurls = [
      # '/rais/2002/<bra>/<cnae>/<cbo>/?id=1',
      # '/secex/2013/<bra>/<hs>/<wld>/?id=1',
      # '/ei/2013/<bra>/<cnae>/<bra>/<cnae>/<hs>/?id=1',
      # '/lattes/all/<bra>/<res>/<ins>/?id=1',
    ].filter (url) ->
      not build? or url.indexOf('/' + build.dataset + '/') is 0

    filterPart = '<' + filterType + '>'
    queries = for dataurl in dataurls
      hasShow = false
      if index?
        idxs = getIndices filterPart, dataurl
        if index < idxs.length
          hasShow = true
          dataurl = replaceStart dataurl, filterPart, 'show', idxs[index]
      filtered = false
      for attr in lockedAttrs
        str = '<' + attr.type + '>'
        if dataurl.indexOf(str) >= 0
          dataurl = dataurl.replace(str, attr.id)
          filtered = true
      continue if not filtered
      if not hasShow
        continue if dataurl.indexOf(filterPart) < 0
        dataurl = dataurl.replace filterPart, 'show'
      dataurl.replace(/<(.*?)>/g,'all')

    if queries.length is 0
      cb null, null
      return
    q = queue()
    for query in queries
      console.log 'executing query for', filterType, query
      q.defer d3.json, query
    q.awaitAll (error, results) ->
      if error
        console.log error
        cb null, null
        return
      possibleIds = {}
      for result in results
        result = result.data
        possibleIds[id] = true for [id, weight] in result
      type2possibleids[filterType] = possibleIds
      cb null, possibleIds

  getAvailableBuildsAndTypes = () ->
    b = []
    t = {}
    for build in builds
      filters = build.filter_types.slice(0)
      includeBuild = true
      for attr in lockedAttrs
        idx = removeValue filters, attr.type
        includeBuild = includeBuild and idx >= 0
      if includeBuild
        b.push build
        t[type] = true for type in filters
    return [b, t]

  createInput = (input, attr, type) ->

    placeholder = if type then dataviva.dict[type] else dataviva.dict.search
    inner = input.append "input"
      .attr "type", "searchText"
      .classed typeahead:true
      .attr "placeholder", placeholder
      .on "focus", () -> d3.select(this).attr "placeholder", ""
      .on "blur", () -> d3.select(this).attr "placeholder", placeholder

    if attr?

      t = attr.type
      if t isnt "bra" and (t isnt "wld" or attr[t+"_id"].length is 2)
        bgColor = attr.color
      else
        bgColor = "none"

      input.append "span"
        .attr "class", "icon"
        .style "background-image", "url("+attr.icon+")"
        .style "background-color", bgColor

      input.append "span"
        .attr "class", "close"

    $(inner.node()).typeahead(
      {minLength: 0, highlight: true, hint:true, autoselect:true},
      name: 'search-freely'
      displayKey: (row) -> row.attr.name
      source: do (attr) -> (text, cb) ->
        clearTimeout timeoutID
        timeoutID = setTimeout () ->
          t = if attr? then attr.type else type
          source text, t, null, lockedBuild, cb
        , delay
      templates:
        empty: '<span class="suggestion">No matches found.</span>'
        suggestion: (row) ->
          prefix = ''
          suffix = ''
          if row.first? and !type
            prefix = '<span class="suggestion-header">'
            prefix += dataviva.dict[row.attr.type+"_plural"] + '</span>'
          if row.left? and !type
            suffix = '<span class="suggestion-footer">'
            suffix += '... and ' + row.left + ' more</span>'
          core = "<span class='suggestion'>" + row.attr.name + "</span>"
          return prefix + core + suffix
    ).focus () ->
      val = $(this).typeahead 'val'
      if val is ''
        $(this).typeahead 'val', '.'
        $(this).typeahead 'val', ''
    .on 'typeahead:selected typeahead:autocompleted', (ev, row) ->
      lockedAttrs.push row.attr # update state
      type2possibleids = {} # reset the cache
      updateSuggestion() # update the suggestion UI element

    if attr?
      $(inner.node()).val attr.name
      inner.attr 'disabled', true
      input.on d3plus.client.pointer.click, do (attr) -> () ->
        removeValue lockedAttrs, attr # update state
        type2possibleids = {} # reset the cache
        updateSuggestion() # update the suggestion UI element

  generalBuild = () ->

    removeBuild.style "display", "none" # hide the close button
    loadBuild.style 'display', "none" # hide the build button

    searchBox.html ''
      # .append("span").html "Search"

    if d3.keys(availTypes).length > 0
      attrs = lockedAttrs.concat null
    else
      attrs = lockedAttrs

    for attr in attrs

      input = searchBox.append "span"
        .attr "class", "lockedAttr"

      createInput(input, attr)

    # focus on the first non-disabled input
    if not firstLoad
      $(document).find('input:enabled.tt-input').first().focus()
    firstLoad = false

  selectBuild = (build) ->

    lockedBuild = build
    window.scrollTo 0, 0
    d3.select(opts.input).node().parentNode.scrollTop = 0

    title = build.stem
    for type in build.filter_types
      span = "<span data-type='"+type+"'></span>"
      title = title.replace(new RegExp("\<"+type+"(.*)\>", "gm"), span)

    searchBox.html title

    for type in build.filter_types

      attrs = (attr for attr in lockedAttrs when attr.type is type)

      input = searchBox.selectAll "span[data-type='" + type + "']"
        .attr "class", "lockedAttr"
        .each (d,i) ->
          attr = if i < attrs.length then attrs[i] else undefined
          createInput(d3.select(this), attr, type)

    removeBuild.style 'display', "inline-block"

    if lockedBuild.completion is 1
      loadBuild.style 'display', "inline-block"
        .attr "href", if opts.callback then null else lockedBuild.url
        .on d3plus.client.pointer.click, () ->
          dataviva[opts.callback](lockedBuild) if opts.callback
    else
      loadBuild.style "display", "none"

    # focus on the first non-disabled input
    $(document).find('input:enabled.tt-input').first().focus()

  updateSuggestion = () ->

    jsonPost = ""
    for a, i in lockedAttrs
      jsonPost += if i is 0 then "?" else "&"
      jsonPost += a.type + "=" + a[a.type + "_id"]

    d3.json "/search/results/" + jsonPost, (error, data) ->

      builds   = data.builds
      profiles = data.profiles

      [availBuilds, availTypes] = getAvailableBuildsAndTypes()

      if opts.profiles

        defaultImage = "/static/img/bgs/triangles.png"

        profileButtons = profileSuggestions.selectAll ".poster"
          .data profiles, (d) -> d.stem

        profileEnter = profileButtons.enter().append "div"
          .attr "class", "poster"

        profileEnter.append "span"
          .attr "class", "title"
          .append("h4")

        profileButtons.order()
          .style "background-image", (d) ->

            if lockedBuild
              sameStem = lockedBuild.stem is d.stem
              lockedBuild = d if sameStem

            subData = if d.subtitle then [d.subtitle] else []

            d3.select(this).select(".title h4").text d.title
            sub = d3.select(this).select(".title").selectAll("sub")
              .data subData

            sub.enter().append("sub")
            sub.text String
            sub.exit().remove()

            if d.image and d.completion is 1
              img = d.image.url
            else
              img = defaultImage

            "url(" + img + ")"

          .on 'click', (d) ->
            selectBuild d

        profileButtons.exit().remove()

      if opts.builds

        dataBuilds = availBuilds.reduce (obj, build) ->
          dataset = build.data_type
          obj[dataset] = [] if dataset not of obj
          obj[dataset].push(build)
          return obj
        , {}

        sections = buildSuggestions.selectAll("div")
          .data(d3.keys(dataBuilds), (d) -> d)

        sections.enter().append("div")
          .append("h2").text (d) -> dataviva.dict[d+"_search"]

        sections.exit().remove()

        sections.each (d) ->
          sectionBuilds = dataBuilds[d]

          buildButtons = d3.select(this)
            .selectAll ".searchBuild"
            .data sectionBuilds, (d) ->
              d.app_type + "_" + d.stem

          buildButtons.enter().append "div"

          buildButtons.order()
            .attr 'class', (d) ->
              if lockedBuild
                sameStem = lockedBuild.stem is d.stem
                if lockedBuild.app_type is d.app_type and sameStem
                  lockedBuild = d
              active = if d.completion is 1 then " active" else ""
              'searchBuild decision icon ' + d.app_type + active
            .html (d) ->
              d.title
            .on 'click', (d) ->
              selectBuild d

      if lockedBuild then selectBuild(lockedBuild) else generalBuild()

  source = (text, specificType, index, build, cb) ->

    cb [{attr: {name:"Loading possible values..."}}]

    [availBuilds, availTypes] = getAvailableBuildsAndTypes()

    text = dataviva.removeAccents text.trim()

    types = if specificType? then [specificType] else attr_types
    types = types.filter (type) -> type of availTypes

    if text.length is 0
      attrResults = []
      ncompletedcalls = 0

      for attrtype in types
        do (attrtype) ->
          getPossibleIds attrtype, index, build, (err, ids) ->
            attrs = type2attrs[attrtype].filter (attr) ->
              not ids? or attr.id of ids
            if ids? then console.log attrtype, Object.keys(ids).length
            # take the top K entries from each type
            nrows = Math.ceil topK/types.length
            for topattr, i in attrs[...nrows]
              row = {attr:topattr}
              row.first = true if types.length > 1 and i is 0
              row.left = attrs.length - nrows if i is nrows - 1
              attrResults.push row
            ncompletedcalls += 1
            if ncompletedcalls is types.length or attrs.length > 0
              cb attrResults
      return

    q = queue()

    # make an async calls to the db for each attribute type
    q.defer getPossibleIds, attrtype, index, build for attrtype in types

    # search each word separately
    words = text.split /[ ,]+/

    # maintain an aggregate score for every attribute across all the words in
    # the query text
    id2attrScore = {}
    for word in words
      for attrtype in types
        # perform fuzzy search for that word
        wordResults = type2fuse[attrtype].search word
        for {item:attr, score} in wordResults
          globalid = attr.type + "|" + attr.id
          if globalid not of id2attrScore
            id2attrScore[globalid] = [attr, 0]
          # update aggregate score for that attribute
          id2attrScore[globalid][1] += (1-score)

    q.awaitAll (error, results) ->
      scoreAttr = []
      # allow only attributes that have data in the db.
      for globalid, [attr, score] of id2attrScore
        idx = types.indexOf attr.type
        if not results[idx]? or attr.id of results[idx]
          scoreAttr.push [score, attr]
      # sort attributes by scores
      scoreAttr.sort ([scoreA, attrA], [scoreB, attrB]) ->
        # if equal scores, prefer higher rank (lower rank number)
        if scoreA is scoreB then return attrA.rank - attrB.rank
        return scoreB - scoreA # prefer higher scores
      nrows = topK
      attrResults = []
      # don't show more than N results
      for [score, topattr], i in scoreAttr[...nrows]
        row = {attr:topattr}
        row.left = scoreAttr.length - nrows if i is nrows - 1
        attrResults.push row
      cb attrResults

  updateSuggestion()
