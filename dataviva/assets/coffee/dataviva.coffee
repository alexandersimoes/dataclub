WARNING = "This file was compiled from coffeescript. Do not edit the .js file!"

window.dataviva = {
  "depths": {}
}

dataviva.cleanData = (data, attr, attr_key, group, url) ->

  demo = url and url.indexOf("/attrs/d/") >= 0
  depths = dataviva.depths[attr]
  if ["bra_s", "bra_r", "cnae_s", "cnae_r"].indexOf(attr_key) >= 0
    split_key = attr_key.split("_")
    id_key = split_key[0] + "_id_" + split_key[1]
  else if demo
    id_key = "id"
  else
    id_key = attr + "_id"

  returnData = data.data.map (d) ->

    dataObj = d.reduce((obj, value, i) ->
      header = data.headers[i]
      header = id_key if header is "id"
      obj[header] = value
      obj
    , {})

    if "month" of dataObj
      dataObj.month = new Date dataObj.year + "/" + dataObj.month + "/01"

    unless demo

      data_id = dataObj[id_key]
      d = depths.slice(0, depths.indexOf(data_id.length) + 1)
      for depth in d
        dataObj[attr + "_" + depth] = data_id.slice(0, depth)

    dataObj

  if attr_key is "course_sc" and not group
    allowedSC = ["xx016","xx017","xx018","xx019","xx020","xx021","xx022"]
    returnData = returnData.filter (d) -> allowedSC.indexOf(d.course_sc_id) < 0

  if group
    if demo
      returnData = returnData.reduce((obj, value) ->
        obj[value.id] = value
        obj
      , {})
    else
      returnData = returnData.reduce((obj, value) ->
        length = value[id_key].length
        id = value[id_key].slice(0, length)
        value[attr + "_" + length] = id
        delete value[data.weight] if data.weight
        obj[attr + "_" + length] = {} unless obj[attr + "_" + length]
        obj[attr + "_" + length][id] = value
        obj
      , {})

  returnData

dataviva.flash = (text) ->

  d3.selectAll("#server_message").remove()

  d3.select("header").append("div")
    .attr "id", "server_message"
    .html text

  setTimeout (->
    d3.selectAll("#server_message").transition().duration(600)
      .style("opacity",0).remove();
  ), 3000

dataviva.lightbox = (content, opts) ->

  if content

    opts   = {} unless opts
    width  = opts.width or window.innerWidth - 80
    height = opts.height or window.innerHeight - 80

    d3.select("body").append "div"
      .attr "class", "shield"
      .on d3plus.client.pointer.click, () -> dataviva.lightbox()

    lightbox = d3.select("body").append "div"
      .attr "class", "lightbox"
      .style "width", width+"px"
      .style "height", height+"px"
      .style "left", (window.innerWidth-width)/2+"px"
      .style "top", (window.innerHeight-height)/2+"px"

    if typeof content is "function"
      content lightbox
    else
      lightbox.html content

  else
    d3.select(".shield").remove()
    d3.select(".lightbox").remove()

dataviva.loading = (parent) ->

  self = this

  @div = d3.select(parent).append("div").attr "class", "loading"
  @icon = self.div.append("i").attr("class", "fa fa-certificate fa-spin")
  @words = self.div.append("div").attr("class", "text")
  @timing = parseFloat(self.div.style("transition-duration"), 10) * 1000

  @show = (callback) ->
    self.div.style "display", "block"
    setTimeout (->
      self.div.style "opacity", 1
      setTimeout callback, self.timing if callback
      return
    ), 5
    self

  @hide = ->
    self.div.style "opacity", 0
    setTimeout (->
      self.div.style "display", "none"
      return
    ), self.timing
    self

  @text = (text) ->
    self.words.html text
    self

  @color = (color) ->
    self.div.style "color", color
    self

  unless Modernizr.cssanimations
    elem = @icon.node()
    degree = 0
    timer = undefined
    rotate = ->
      degree = 0  if degree is 360
      elem.style.msTransform = "rotate(" + degree + "deg)"
      elem.style.transform = "rotate(" + degree + "deg)"

      # timeout increase degrees:
      timer = setTimeout(->
        degree = degree + 4
        rotate() # loop it
        return
      , 20)

      return
    rotate()

  this

dataviva.num_format = (number, key, vars) ->
  return "-" unless typeof number is "number"
  number = d3plus.number.format(number, key, vars)
  if key of dataviva.affixes and dataviva.restricted_affixes.indexOf(key) < 0
    a = dataviva.affixes[key]
    number = a[0] + number + a[1]
  number

dataviva.removeAccents = (s) ->
  diacritics = [
    [/[\300-\306]/g, 'A'],
    [/[\340-\346]/g, 'a'],
    [/[\310-\313]/g, 'E'],
    [/[\350-\353]/g, 'e'],
    [/[\314-\317]/g, 'I'],
    [/[\354-\357]/g, 'i'],
    [/[\322-\330]/g, 'O'],
    [/[\362-\370]/g, 'o'],
    [/[\331-\334]/g, 'U'],
    [/[\371-\374]/g, 'u'],
    [/[\321]/g, 'N'],
    [/[\361]/g, 'n'],
    [/[\307]/g, 'C'],
    [/[\347]/g, 'c'],
  ]
  for i in [0...diacritics.length]
    s = s.replace diacritics[i][0], diacritics[i][1]
  return s

dataviva.restricted_affixes = ["num_emp", "students", "enrolled",
                               "graduates", "entrants"]

dataviva.search = (input, opts) ->

  opts = {} unless opts
  icon = d3.select(input.node().parentNode).select("i")

  datatypes  = opts.attr or ["bra", "hs", "wld", "cnae", "cbo", "course_hedu", "university"]
  datatypes  = [datatypes] unless datatypes instanceof Array
  threshold  = 0.3 # threshold for the fuzzy search
  delay      = 100 # delay in ms, so search won't be called while typing
  timeoutID  = null
  weights    = {}
  type2attrs = {}
  type2fuse  = {}
  attrs      = []

  restricted =
    hs:   [2, 6]
    cnae: [1, 6]
    cbo:  [1, 4]

  input.on "click.load", () -> initSearch()

  initSearch = () ->

    input.on "click.load", null

    q = queue()

    for t in datatypes
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

        if type of restricted
          subattrs = subattrs.filter (d) ->
            restricted[type].indexOf(d[type+"_id"].length) >= 0

        # sort attributes by weight
        weight = weights[type]
        subattrs = subattrs.filter (a) -> a[weight]
        subattrs.sort (a,b) ->
          if b[type+"_id"].length is a[type+"_id"].length
            b[weight] - a[weight]
          else
            b[type+"_id"].length - a[type+"_id"].length

        for attr, i in subattrs
          attr.rank = i
          attr.type = type
          attr.url = "/profile/" + type + "/" + attr[type+"_id"] + "/"
          attr.id = attr[type+"_id"]
          attr.normName = dataviva.removeAccents attr.name
          attrs.push attr

        # initialize local fuse for each attribute type
        type2fuse[type] = new Fuse subattrs, {
          keys:         ["normName", "id"],
          includeScore: true,
          threshold:    threshold
        }

      $(input.node()).typeahead(
        {minLength: 1, highlight: false, hint:true, autoselect:true},
        # name: 'search-freely'
        displayKey: (row) -> row.attr.name
        source: do (attr) -> (text, cb) ->
          clearTimeout timeoutID
          timeoutID = setTimeout () ->
            source text, cb
          , delay
        templates:
          empty: "<div class='tt-suggestion'>No matches found.</div>"
          suggestion: (row) ->
            w = weights[row.attr.type]
            t = row.attr.type
            i = row.attr[t+"_id"]
            image = row.attr.icon
            color = if t is "bra" or (t is "wld" and i.length is 5) then "transparent" else row.attr.color
            image = if image then "<span class='icon' style='background-color:"+color+"'><img src='" + image + "'></span>" else ""
            title = "<span class='title'>" + image + row.attr.name + "</span>"
            type = if t is "bra" then dataviva.dict[t+"_"+i.length] else dataviva.dict[t]
            type = "<span class='sub'>" + type + ": " + i + "</span>"
            weight = dataviva.num_format row.attr[w], w
            weight = "<span class='sub'>" + dataviva.dict[w] + ": " + weight + "</span>"
            return title + type + weight
        # templates:
        #   empty: '<span class="suggestion">No matches found.</span>'
        #   suggestion: (row) ->
        #     prefix = ''
        #     suffix = ''
        #     if row.first? and !type
        #       prefix = '<span class="suggestion-header">'
        #       prefix += dataviva.dict[row.attr.type+"_plural"] + '</span>'
        #     if row.left? and !type
        #       suffix = '<span class="suggestion-footer">'
        #       suffix += '... and ' + row.left + ' more</span>'
        #     core = "<span class='suggestion'>" + row.attr.name + "</span>"
        #     return prefix + core + suffix
        )
        .on "typeahead:selected typeahead:autocompleted", (ev, row) ->
          if row
            input.attr "disabled", true
            icon.attr "class", "fa fa-spinner fa-spin"
            window.location = row.attr.url

      $(input.node().parentNode).find('input:enabled.tt-input').first().focus()

  source = (text, cb) ->

    cb [{attr: {name:"Loading..."}}]

    # search each word separately
    words = text.split /[ ,]+/

    # maintain an aggregate score for every attribute across all the words in
    # the query text
    id2attrScore = {}
    for word in words
      for attrtype in datatypes
        # perform fuzzy search for that word
        wordResults = type2fuse[attrtype].search word
        for {item:attr, score} in wordResults
          globalid = attr.type + "|" + attr.id
          if globalid not of id2attrScore
            id2attrScore[globalid] = [attr, 0]
          # update aggregate score for that attribute
          id2attrScore[globalid][1] += (1-score)

    scoreAttr = []
    # allow only attributes that have data in the db.
    for globalid, [attr, score] of id2attrScore
      idx = datatypes.indexOf attr.type
      scoreAttr.push [score, attr]
    # sort attributes by scores
    scoreAttr.sort ([scoreA, attrA], [scoreB, attrB]) ->
      # if equal scores, prefer higher rank (lower rank number)
      if scoreA is scoreB then return attrA.rank - attrB.rank
      return scoreB - scoreA # prefer higher scores
    nrows = 5
    attrResults = []
    # don't show more than N results
    for [score, topattr], i in scoreAttr[...nrows]
      row = {attr:topattr}
      row.left = scoreAttr.length - nrows if i is nrows - 1
      attrResults.push row
    cb attrResults

dataviva.tooltip = (elems, align) ->

  elems = d3.selectAll(".alt_tooltip") unless elems

  elems
    .on d3plus.client.pointer.over, () ->
      tooltip this, align
    .on d3plus.client.pointer.out, () ->
      tooltip false

  tooltip = (elem, align) ->

    d3plus.tooltip.remove "alt_tooltip"

    if elem

      size = elem.getBoundingClientRect()
      text = elem.getAttribute("alt")
      text = dataviva.dict[text] if text of dataviva.dict

      align = "bottom center" unless align

      t = align.split(" ")[0]
      offset = if t is "center" then size.width/2 else size.height/2

      d3plus.tooltip.create
        x:           size.left+size.width/2+window.scrollX,
        y:           size.top+size.height/2+window.scrollY,
        offset:      offset,
        arrow:       true,
        description: text,
        width:       "auto",
        id:          "alt_tooltip",
        align:       align,
        max_width:   400

dataviva.url = (build, page) ->

  if Modernizr.history

    page    = "builder" unless page
    url     = build.url.replace("/build/", "/" + page + "/")
    title   = build.title
    replace = window.location.pathname.indexOf(url.split("?")[0]) >= 0

    document.title = "DataViva : " + title if title

    if replace
      window.history.replaceState
        prev_request: url
      , title, url
    else
      window.history.pushState
        prev_request: url
      , title, url

  return
