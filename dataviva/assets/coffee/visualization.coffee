WARNING = "This file was compiled from coffeescript. Do not edit the .js file!"

visualizations = {}
dataCache = {}
trackedAttrs = {}
page = location.pathname.split("/")[1]

datasetDefault =
  rais:  "num_emp"
  secex: "export_val"
  ei:    "purchase_value"
  sc:    "enrolled"
  hedu:  "enrolled"

demoURL = "/attrs/d/?lang="+dataviva.language

locale = if dataviva.language is "en" then "en_US" else "pt_BR"

tickSize = 15
defaultStyle =
  aggs:
    wage_avg: (leaves) ->
      wage = d3.sum leaves, (d) -> d.wage
      num_emp = d3.sum leaves, (d) -> d.num_emp
      wage/num_emp
  background: "#fafafa"
  font:
    family: "Oswald"
    weight: 400
  format:
    locale: locale
    number: dataviva.num_format
    text: (text, key, vars) ->
      return "Male" if text is "A" and key is "d_id"
      return "Female" if text is "B" and key is "d_id"
      return dataviva.dict[vars.id.value+"_plural"] if key is "threshold"
      return dataviva.dict[text] if text of dataviva.dict
      d3plus.string.title text, key, vars
  legend:
    size: [24, 24]
  title:
    font:
      size: 24
    sub:
      font:
        size: tickSize
    total:
      font:
        size: tickSize
  x:
    axis:
      color: "#ccc"
      font:
        size: tickSize
    grid: false
    label:
      font:
        size: 24
    ticks:
      font:
        size: tickSize
  y:
    axis:
      color: "#ccc"
      font:
        size: tickSize
    grid: false
    label:
      font:
        size: 24
    ticks:
      font:
        size: tickSize
  zoom:
    scroll: false


# Smartly overwrites d3plus configuration object keys.
configMerge = (oldParams, newParams) ->
  for method of newParams
    if method of oldParams
      preset = oldParams[method]
      value  = newParams[method]
      if method is "ui"
        for ui in method
          match = preset.filter (m) -> m.method is ui.method
          unless match.length
            oldParams[method].push ui
      else
        unless d3plus.object.validate(preset)
          preset = {value: preset}
        if d3plus.object.validate(value)
          preset = d3plus.object.merge(preset, value)
        else
          preset.value = value
        oldParams[method] = preset
    else
      oldParams[method] = newParams[method]
  oldParams

# Sets all of the d3plus.viz params dependent on the build.
config = (build) ->

  params = {}

  output = build.display_attr
  depths = dataviva.depths[output].slice()
  if depths.length > 2
    mod = if build.data_type is "ei" and output is "cnae" then 2 else 1
    if output isnt "bra"
      depths = [depths[0], depths[depths.length - mod]]
    else
      depths.shift()
      if build.data_type isnt "ei"
        bras = build.filter_ids.bra.map (b) ->
          if b is "sabra" then 0 else b.length
        bras = d3.min bras
        depths = depths.filter (d) -> d > bras
        if depths.length > 1
          depths = [depths[0], depths[depths.length-1]]
  network = dataCache[build.network] if build.network

  if build.app_type is "tree_map"
    size = build.config.size or datasetDefault[build.data_type]
    if dataviva.restricted_affixes.indexOf(size) >= 0 and size of dataviva.affixes
      a = dataviva.affixes[size]
      total = {prefix: a[0], suffix: a[1]}
    else
      total = true

    params =
      data:
        padding: 0
      labels:
        align: "start"
      title:
        total: total
      type: "tree_map"

    params.depth = 0 if build.data_type is "ei" and output is "bra"

  else if build.app_type is "geo_map"

    params =
      color: datasetDefault[build.data_type]
      coords: dataCache[build.coords]
      type: "geo_map"

  else if build.app_type is "stacked"

    params =
      depth: 0
      shape:
        interpolate: "monotone"
      timeline: false
      type: "stacked"
      x: "year"
      y: datasetDefault[build.data_type]

  else if build.app_type is "line"

    params =
      depth: 0
      shape:
        interpolate: "monotone"
      timeline: false
      type: "line"
      x: "year"
      y:
        scale: "linear"
        value: datasetDefault[build.data_type]

  else if build.app_type is "network"

    params =
      active:
        spotlight: true
        value: (d) -> d.rca >= 1
      depth: depths[depths.length-1]
      edges: network.edges
      labels: false
      nodes: network.nodes
      size:
        scale: d3.scale.pow().exponent(3 / 8)
      title:
        sub: "Click to zoom"
      type: "network"

  else if build.app_type is "rings"

    params =
      depth: depths[depths.length-1]
      edges: network.edges
      nodes: network.nodes
      size:  false
      type:  "rings"

  else if build.app_type is "scatter"

    url = build.data_url.split("/")
    url[3] = "all"
    url[2] = 2013 if build.data_type is "secex"
    url = url.join("/")

    params =
      active:
        spotlight: true
        value: (d) -> d.rca >= 1
      dataMerge: (data, extra) ->

        output = build.display_key + "_id"

        for d in data
          ex = extra.filter((e) -> e[output] is d[output] )[0]
          d.pci = ex.pci if "pci" of ex

        data

      depth: 0
      extraData: url
      labels: false
      type: "scatter"
      x: "distance"
      y: if output is "cnae" then "cbo_diversity_eff" else "pci"

  else if build.app_type is "compare"

    params =
      labels: false
      type: "scatter"

  else if build.app_type is "occugrid"

    url = build.data_url.split("/")
    url[3] = "all"
    url = url.join("/")

    params =
      active:
        spotlight: true
        value: "mne_medium"
      dataMerge: (data, extra) ->

        keys = ["mne_micro", "mne_small", "mne_medium",
                "mne_large", "age_avg", "wage_avg"]

        data.filter (d) ->

          bra = extra.filter((e) -> e.cbo_id is d.cbo_id )[0]

          keys.forEach (key) ->
            if key.indexOf("mne") is 0
              d[key] = Math.ceil(d[key])
              d[key + "_bra"] = Math.ceil(bra[key])
            else
              d[key + "_bra"] = bra[key]
            return
          d.importance = bra.importance
          bra.importance > 0.25

      extraData: url
      id:
        grouping: false
      size: "importance"
      total: "mne_medium_bra"
      type: "bubbles"

  else if build.app_type is "bar"

    params =
      order:
        agg: "max"
        sort: "desc"
      type: "bar"
      y:
        scale: "linear"

    if build.demo
      params.x =
        ticks:
          font:
            size: 13

  else if build.app_type is "pie"

    params =
      type: "pie"

  else if build.app_type is "box"

    params =
      type:
        mode: [0, 100]
        value: "box"

  nesting = []

  data = dataCache[build.data_url]

  if build.demo
    attrs = dataCache[demoURL]
    key = output + "_" + depths[depths.length - 1]

    if build.app_type is "bar"
      if build.demo is "gender"
        if build.config.order and build.config.order.indexOf(".") > 0
          gender = build.config.order.split(".")[1]
        else
          gender = "A"
        ordering = if gender is "A" then ["A", "B"] else ["B", "A"]
        data.sort (a, b) -> ordering.indexOf(a.d_id) - ordering.indexOf(b.d_id)
      else if build.demo is "ethnicity"
        ordering = ["D", "H", "G", "E", "F", "C"]
        data.sort (a, b) -> ordering.indexOf(a.d_id) - ordering.indexOf(b.d_id)
      build.config.x = output

    for d in data
      attr = dataCache[build.attr_url][key][d[key]]
      demoAttr = dataCache[demoURL][d.d_id]
      d[output] = attr.name
      d.name = demoAttr.name

    depths = ["d_id"]

    if build.app_type is "stacked"
      params.size =
        threshold: false
      params.y =
        scale:  "share"
        values: params.y

  else
    attrs = dataCache[build.attr_url]

  iconStyle  = {}
  textLabels = {}
  for d, i in depths
    level = if d isnt "d_id" then output + "_" + d else d
    if level.indexOf("bra") == 0 or level is "wld_5"
      iconStyle[level] = "default"
    else
      iconStyle[level] = "knockout"
    textLabels[level] = ["name", level]
    nesting.push level

  defaults =
    attrs: attrs
    color: "color"
    data:  data
    depth: nesting.length - 1
    icon:
      style: iconStyle
      value: "icon"
    id: nesting
    size: datasetDefault[build.data_type]
    text: textLabels
    time: "year"

  defaults.focus =
    tooltip: (["embed", "builder"].indexOf(page) >= 0 or
              build.container.classed("lightbox"))

  if build.config.y is "trade_val"

    defaults.data = defaults.data.reduce (arr, d, i) ->
      export_data = d3plus.util.copy d
      export_data.trade_val = export_data.export_val
      export_data.flow = "export_val"
      export_data.color = "#0b1097"
      delete export_data.export_val
      delete export_data.import_val
      import_data = d3plus.util.copy d
      import_data.trade_val = import_data.import_val
      import_data.flow = "import_val"
      import_data.color = "#c8140a"
      delete import_data.export_val
      delete import_data.import_val
      arr.push export_data
      arr.push import_data
      arr
    , []
    defaults.id.push "flow"
    params.depth = defaults.id.length - 1
    params.color = "color"
    defaults.text = "flow"
    params.y.label = dataviva.dict["export_import"]

  else if build.config.y is "trade_net"

    for d in defaults.data
      d.export_val = 0 unless d.export_val
      d.import_val = 0 unless d.import_val
      d.trade_net = d.export_val - d.import_val

  if build.config.split

    if build.config.split is "time"
      times =
        morning: "#f7b6d2"
        afternoon: "#ffc41c"
        night: "#2f2f6d"
        full_time: "#105b10"
      defaults.data = defaults.data.reduce (arr, d, i) ->
        for t, color of times
          data_obj = d3plus.util.copy d
          for t2, c2 of times
            delete data_obj[t2]
          data_obj.enrolled = d[t]
          data_obj.name = t
          data_obj.color = color
          data_obj.icon = "/static/img/icons/time/time_"+t+".png"
          arr.push data_obj
        arr
      , []
      defaults.id = ["name"]
      defaults.icon.style["name"] = "knockout"
      params.depth = 0

      if build.app_type is "stacked"
        params.size =
          threshold: false
        params.y =
          scale:  "share"
          values: params.y

    delete build.config.split

  if defaults.id[0].indexOf("university") is 0
    params.legend = false
    if "size" of params
      if d3plus.object.validate params.size
        params.size.threshold = false
      else
        params.size =
          threshold: false
          value: params.size
    else
      params.size =
        threshold: false

  defaults.ui = []
  if page isnt "profile"

    depthToggle = defaults.id.reduce (arr, n, i) ->
      obj = {}
      obj[n] = i
      arr.push obj
      arr
    , []

    if build.data_type is "secex"

      if output is "hs"
        colorToggle = ["color", "pci", "opp_gain", "opp_gain_wld",
                       "export_val_growth", "export_val_growth_5",
                       "import_val_growth", "import_val_growth_5"]
      else
        colorToggle = ["color", "eci", "hs_diversity", "hs_diversity_eff",
                       "export_val_growth", "export_val_growth_5",
                       "import_val_growth", "import_val_growth_5"]

    else if build.data_type is "rais"

      if build.app_type is "tree_map"
        sizeMethod = "size"
        sizeToggle = ["num_emp", "wage", "num_est"]
      else if build.app_type is "occugrid"
        sizeMethod = (value, viz) ->
          if value is "mne"
            viz.size(viz.total()).draw()
          else
            viz.size(value).draw()
        sizeToggle = ["importance", "wage_avg", "wage_avg_bra", "mne"]
      else
        sizeMethod = "size"
        sizeToggle = ["num_emp", "wage", "wage_avg", "num_est"]

      if output is "cnae"
        colorToggle = ["color", "cbo_diversity", "cbo_diversity_eff",
                       "opp_gain", "wage_growth", "wage_growth_5",
                       "num_emp_growth", "num_emp_growth_5"]
      else
        colorToggle = ["color", "wage_growth", "wage_growth_5",
                       "num_emp_growth", "num_emp_growth_5"]

    else if build.data_type is "ei"

      sizeMethod = "size"
      sizeToggle = ["purchase_value", "tax", "icms_tax"]

    else if build.data_type is "sc"

      sizeMethod = "size"
      sizeToggle = ["enrolled", "classes"]

    else if build.data_type is "hedu"

      sizeMethod = "size"
      sizeToggle = ["enrolled", "graduates", "entrants"]

      defaults.ui = []

    if sizeToggle and build.app_type is "geo_map"
      defaults.ui.push
        label: dataviva.dict.color
        method: "color"
        value: sizeToggle
    else
      if sizeToggle and build.app_type isnt "rings"
        defaults.ui.push
          label: dataviva.dict.size
          method: sizeMethod
          value: sizeToggle
      if colorToggle
        defaults.ui.push
          label: dataviva.dict.color
          method: "color"
          value: colorToggle

    if build.app_type isnt "geo_map" and
       build.app_type isnt "network" and
       build.app_type isnt "rings" and
       depthToggle.length > 1
      defaults.ui.push
        label: dataviva.dict.depth
        method: "depth"
        value: depthToggle

    if build.app_type is "scatter"
      defaults.ui.push
        label: dataviva.dict.x
        method: "x"
        value: ["distance", "opp_gain"]

      if build.data_type is "rais"
        defaults.ui.push
          label: dataviva.dict.y
          method: "y"
          value: ["cbo_diversity_eff", "cbo_diversity", "opp_gain"]
      else if build.data_type is "secex"
        defaults.ui.push
          label: dataviva.dict.y
          method: "y"
          value: ["pci", "opp_gain"]

    if build.app_type is "compare"

      defaults.ui.push
        label: dataviva.dict.scale
        method: (value, viz) ->
          viz.x({"scale": value}).y({"scale": value}).draw()
        value: ["log", "linear"]

      if build.data_type is "rais"
        defaults.ui.push
          label: dataviva.dict.axes
          method: (value, viz) -> viz.x(value).y(value).draw()
          value: ["num_emp", "wage", "wage_avg", "num_est"]

    if build.app_type is "network" or
       build.app_type is "rings" or
       build.app_type is "scatter"
      defaults.ui.push
        label: dataviva.dict.spotlight
        method: (value, viz) ->
          value = if value then true else false
          viz.active({"spotlight": value}).draw()
        value: [{"on": 1}, {"off": 0}]

      defaults.ui.push
        label: dataviva.dict.rca_scope
        method: (value, viz) ->
          viz.active((d) -> d[value] >= 1).draw()
        value: ["bra_rca", "wld_rca"]

    if build.app_type is "stacked"

      defaults.ui.push
        label: dataviva.dict.sort
        method: (value, viz) -> viz.order({"sort": value}).draw()
        value: ["asc", "desc"]

      defaults.ui.push
        label: dataviva.dict.layout
        method: (value, viz) -> viz.y({"scale": value}).draw()
        value: ["linear", "share"]

    if build.app_type is "occugrid"
      defaults.ui.push
        label: dataviva.dict.grouping
        method: (value, viz) ->
          grouping = value is "category"
          viz.id({"grouping": grouping}).draw()
        value: ["id", "category"]

    if build.app_type is "stacked" or build.app_type is "occugrid"
      defaults.ui.push
        label: dataviva.dict.order
        method: (value, viz) ->
          value = viz.text() if value is "name"
          value = viz.size() if value is "value"
          value = viz.color() if value is "color"
          viz.order(value).draw()
        value: ["name", "value", "color"]

  if build.app_type is "line" or build.app_type is "bar"
    defaults.ui.push
      label: dataviva.dict.y_scale
      method: (value, viz) ->
        viz.y({"scale": value}).draw()
      value: ["linear", "log"]
  if build.demo and build.app_type is "bar" and build.data_type is "rais"
    defaults.ui.push
      label: dataviva.dict.y
      method: "y"
      value: ["wage_avg", "num_emp"]

  params = configMerge(defaults, params)

  if build.config.order
    if build.demo and build.data_type is "sc" and build.app_type is "bar"
      build.config.order = "course_sc_5"
    else
      build.config.order = true

  params = configMerge(params, build.config)

  build.configured = true

  params

# Handles all of the logic for loading attrs/data, and then passes the builds
# off to the draw() function to be rendered on the page.
window.visualization = (builds) ->

  # Forces 'builds' variable into an Array.
  builds = [builds]  unless builds instanceof Array

  args = {}

  for build in builds

    build.container = build.container or d3.select("body")
    unless d3plus.util.d3selection(build.container)
      build.container = d3.select(build.container)

    div = build.container
    build.id = div.attr("id") or div.attr("class") or div.node().localName
    div.style "position", "relative" if div.style("position") is "static"

    ui = div.append("div").attr("class", "visualization_ui")

    # Creates a link to the YouTube style build page.
    if page isnt "build"
      ui.append "a"
        .attr "alt", "comments"
        .attr "href", build.url
        .append "i"
          .attr "class", "fa fa-comments"

    # Creates a minimize/maximize button on all non-embedded pages.
    if page isnt "embed"
      if div.classed("lightbox")
        ui.append "a"
          .attr "alt", "minimize"
          .on d3plus.client.pointer.click, (d) ->
            d3plus.tooltip.remove "alt_tooltip"
            dataviva.lightbox()
          .append "i"
            .attr "class", "fa fa-compress"
      else
        ui.append "a"
          .attr "alt", "enlarge"
          .data [build]
          .on d3plus.client.pointer.click, (d) ->
            d3plus.tooltip.remove "alt_tooltip"
            dataviva.lightbox (elem) ->
              copy = d3plus.util.copy(d)
              copy.container = elem
              visualization copy
          .append "i"
            .attr "class", "fa fa-expand"

    uiWidth = ui.node().getBoundingClientRect().width
    titleWidth = div.node().getBoundingClientRect().width - uiWidth * 2
    titleWidth -= 200
    title = if page isnt "build" then build.title else false

    dataviva.tooltip ui.selectAll("a")

    visualizations[build.id] = d3plus.viz()
      .container div.append("div").attr("class", "visualization_d3plus")
      .config defaultStyle
      .error dataviva.dict.loading + "..."
      .margin if div.classed("lightbox") then 10 else 0
      .title
        height: ui.node().getBoundingClientRect().height
        width: titleWidth
        value: title
      .draw()

    attr_type = build.display_attr
    build.attr_url = "/attrs/"+attr_type+"/?lang="+dataviva.language
    build.data_url = "/"+build.url.split("/").slice(3).join("/")

    for attr_type of build.filter_ids

      trackedAttrs[attr_type] = [] unless attr_type of trackedAttrs
      filters = build.filter_ids[attr_type].filter (f) ->
        trackedAttrs[attr_type].indexOf(f) < 0

      if filters.length
        args[attr_type] = [] unless attr_type of args
        args[attr_type] = args[attr_type].concat(filters)
        trackedAttrs[attr_type] = trackedAttrs[attr_type].concat(filters)

  params = ""
  joiner = "?"
  for attr_type of args
    params += joiner+attr_type+"="+d3.set(args[attr_type]).values().join(",")
    joiner = "&"

  if params.length and (builds.length > 1 or not
     builds[0].container.classed("lightbox"))
    setTimeout (->
      d3.json("/account/attr_view" + params).get()
      return
    ), 5000

  finish builds

urlChecks = ["attr_url", "coords", "network", "data_url"]
finish = (builds) ->

  readyBuilds = []

  nextURLs = builds.reduce((obj, build) ->

    if build.demo and (demoURL not of dataCache)
      obj[demoURL] = [] unless obj[demoURL]
      obj[demoURL].push build
      return obj

    for url in urlChecks
      if build[url] and (build[url] not of dataCache)
        obj[build[url]] = [] unless obj[build[url]]
        obj[build[url]].push build
        return obj

    build.config = config(build) unless build.configured
    extraData = build.config.extraData
    if extraData
      if extraData not of dataCache
        obj[extraData] = [] unless obj[extraData]
        obj[extraData].push build
        return obj

      dataCache[build.url] = build.config.dataMerge(
        build.config.data, dataCache[extraData]
      ) if build.url not of dataCache

      build.config.data = dataCache[build.url]
      delete build.config.dataMerge
      delete build.config.extraData
    readyBuilds.push build
    obj
  , {})

  checkData nextURLs
  draw readyBuilds

checkData = (urls) ->

  for url of urls
    builds = urls[url]
    attrURL = url.indexOf("/attrs/") is 0
    attr = if url.indexOf("/attrs/d/") < 0 then builds[0].display_attr else "d"
    stored = attrURL and Modernizr.localstorage and
             url of localStorage and ((attr not of dataviva.storage) or
             (parseFloat(localStorage[attr]) is dataviva.storage[attr]))
    if dataCache[url]
      finish builds
    else if stored
      data = JSON.parse(localStorage[url])
      dataviva.depths[attr] = data.depths
      dataCache[url] = dataviva.cleanData data, attr,
                                          builds[0].display_key, attrURL, url
      finish builds
    else
      loadData url, builds

# Loads data using d3.json. If it is an attr url, it will then load the data
# urls associated with each build. If it is a data url, it will draw the
# visualization for each build.
loadData = (url, builds) ->

  attrURL    = url.indexOf("/attrs/") is 0
  coordURL   = url.indexOf("/coords/") > 0
  networkURL = url.indexOf("/networks/") > 0

  attr = if url.indexOf("/attrs/d/") < 0 then builds[0].display_attr else "d"
  attr_key = builds[0].display_key

  d3.json url, (error, data) ->
    if not coordURL and not networkURL

      # Combines the data and the headers into 1 large array of objects.
      dataviva.depths[attr] = data.depths if attrURL
      dataCache[url] = dataviva.cleanData(data, attr, attr_key, attrURL, url)
    else
      dataCache[url] = data

    # If an attr url was loaded, this puts it in locale storage.
    if attrURL and Modernizr.localstorage
      if attr of dataviva.storage
        localStorage[attr] = dataviva.storage[attr]
        localStorage[url] = JSON.stringify(data)
    finish builds

draw = (builds) ->

  for build in builds

    console.log "D3plus configuration for \""+build.title+"\":"
    console.log build.config

    viz = visualizations[build.id]
      .error false
      .config build.config
      .depth build.config.depth
      .draw()
