WARNING = "This file was compiled from coffeescript. Do not edit the .js file!"

colorLevels = ["primary", "secondary", "tertiary"]
profileColor = {}
d3.select(".image").each () ->
  colors = []
  for level in colorLevels
    color = d3.select(this).attr("data-"+level)
    colors.push color if color
  for c in colors
    if d3.hsl(c).l >= 0.9
      profileColor.light = c
      break
  for c in colors
    if d3.hsl(c).l <= 0.6
      profileColor.dark = c
      break
  profileColor.background = colors[0]
  profileColor.accent = colors[1]
  profileColor.light = "#f7f7f7" unless profileColor.light
  profileColor.dark = "#444" unless profileColor.dark
  if d3.hsl(colors[0]).l > 0.3 and d3.hsl(colors[0]).l < 0.6
    profileColor.labels = colors[0]
  else if d3.hsl(colors[1]).l > 0.3 and d3.hsl(colors[1]).l < 0.6
    profileColor.labels = colors[1]
  else
    profileColor.labels = profileColor.dark

activeSection = false
d3.select("header")
  .style "background-color", profileColor.background
  .each () ->
    text = d3plus.color.text profileColor.background
    if d3.hsl(text).l > 0.5
      if profileColor.light is profileColor.background or
         profileColor.light is profileColor.accent
        profileColor.link = text
      else
        profileColor.link = profileColor.light
      d3.select(this).select("#logo")
        .style "color", "white"
        # .style "background-image", "url('/static/img/nav/DataVivaWhite.png')"
    else
      if profileColor.dark is profileColor.background or
         profileColor.dark is profileColor.accent
        profileColor.link = text
      else
        profileColor.link = profileColor.dark

    d3.select(this).selectAll(".link")
      .style "color", profileColor.link
      .on d3plus.client.pointer.over, () ->
        d3.select(this).style "color", profileColor.accent
      .on d3plus.client.pointer.out, () ->
        d3.select(this).style "color", profileColor.link

    d3.select(this).selectAll("li.depth_1")
      .style "color", profileColor.accent
      .style "background-color", profileColor.background

    d3.select(this).selectAll("li.depth_0, li.depth_2, li.depth_3")
      .style "color", profileColor.link
      .style "background-color", profileColor.background
      .on d3plus.client.pointer.over, () ->
        if this.id isnt "link_"+activeSection
          d3.select(this).style "color", profileColor.accent
      .on d3plus.client.pointer.out, () ->
        if this.id isnt "link_"+activeSection
          color = profileColor.link
        else
          color = d3plus.color.text profileColor.accent
        d3.select(this).style "color", color

d3.selectAll("h1").style "color", (d, i) -> profileColor.labels if i isnt 0
d3.select("main").selectAll("h2, h3").style "color", profileColor.labels

d3.select(".toggleStats")
  .style "background-color", profileColor.background
  .style "color", profileColor.accent
  .on d3plus.client.pointer.over, () ->
    d3.select(this)
      .style "background-color", profileColor.background
      .style "color", profileColor.accent

if d3.hsl(profileColor.background).l > 0.3 and
   d3.hsl(profileColor.background).l < 0.9
  shadowColor = profileColor.background
else if d3.hsl(profileColor.accent).l > 0.3 and
   d3.hsl(profileColor.accent).l < 0.9
  shadowColor = profileColor.accent
else
  shadowColor = profileColor.labels
shadowHSL = d3.hsl(shadowColor)
shadowHSL.l = 0.8
shadowColor = shadowHSL.toString()
shadowStyle = "inset 0px -2px 0 "
d3.selectAll("p").selectAll("a")
  .style "box-shadow", shadowStyle + shadowColor
  .on d3plus.client.pointer.over, () ->
    d3.select(this)
      .style "color", profileColor.labels
      .style "box-shadow", "none"
  .on d3plus.client.pointer.out, () ->
    d3.select(this)
      .style "color", "#444"
      .style "box-shadow", shadowStyle + shadowColor

mainStyle = (link) ->
  link
    .style "background-color", () ->
      if this.id is "link_"+activeSection
        profileColor.accent
      else
        profileColor.background
    .style "color", () ->
      if this.id is "link_"+activeSection
        d3plus.color.text profileColor.accent
      else
        profileColor.accent

subStyle = (link) ->
  link
    .style "background-color", () ->
      if this.id is "link_"+activeSection
        profileColor.accent
      else
        profileColor.background
    .style "color", () ->
      if this.id is "link_"+activeSection
        d3plus.color.text profileColor.accent
      else
        profileColor.link

testPositions = () ->

  if (window.innerHeight + window.scrollY) >= document.body.offsetHeight
    links = d3.selectAll("a.section_link")
    activeLink = links[0][links.size() - 1].id
  else
    activeLink = false
    previousLink = false
    found = false
    top = 0
    d3.selectAll("a.section_link").each (d, i) ->
      start = top if i is 0
      unless found
        top = this.getBoundingClientRect().top
        top += parseFloat(d3.select(this).select("*").style("margin-top"), 10)
        # console.log this.id, top, window.innerHeight
        if top >= -5 and top <= window.innerHeight * 0.25
          activeLink = this.id
          found = true
        else if top > window.innerHeight * 0.25
          activeLink = previousLink
          found = true
        previousLink = this.id
    if !activeLink and top < 0
      links = d3.selectAll("a.section_link")
      activeLink = links[0][links.size() - 1].id

  if activeLink isnt activeSection
    activeSection = activeLink
    d3.selectAll("li.depth_1").transition().duration 200
      .call mainStyle
    d3.selectAll("li.depth_2, li.depth_3").transition().duration 200
      .call subStyle

  i = notLoaded.length
  newBuilds = []
  while i--
    build = notLoaded[i]
    rect = build.container.node().getBoundingClientRect()

    if rect.top < window.innerHeight and rect.bottom > 0
      newBuilds.push build
      notLoaded.splice i, 1

  visualization newBuilds

# Logic for the stat panel show/hide.
d3.select(".stats").each ->

  d3.select(this)
    .attr "data-height", d3.select(this).style("height")
    .style "height", "0px"
    .style "visibility", "visible"

d3.selectAll(".toggleStats")
  .on d3plus.client.pointer.click, ->
    stats = d3.select(".stats")
    active = stats.style("height") is "0px"
    height = if active then stats.attr("data-height") else "0px"
    stats.style "height", height
    d3.select(".headlines").classed "active", active

# Colors the text of each attribute button in the stats based on it's background
# color.
d3.selectAll("a.attr").style "color", (d) ->
  color = d3.select(this).style("background-color")
  d3plus.color.text color


notLoaded = []
d3.selectAll("div.build").each () ->
  build = dataviva.builds[parseFloat(this.id.split("_")[1])]
  build.container = d3.select(this)
  notLoaded.push build

document.onscroll = testPositions
testPositions()
