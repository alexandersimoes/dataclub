WARNING = "This file was compiled from coffeescript. Do not edit the .js file!"

prefix = d3plus.client.prefix()
featuredPage = 0

featureDisplay = (page) ->
  transition = if page is false then 0 else timing
  if featuredPage >= buttons.size() or featuredPage < 0
    featuredPage = 0
  offset = - featuredPage * window.innerWidth
  light = featuredColors[featuredPage].light
  color = if light then light else buttonColor
  buttons.style("background-color", color).classed "active", false
  d3.select("#featured_"+featuredPage).classed "active", true
  d3.select(".featured_link").transition().duration transition
    .style "margin-left", offset+"px"

resizeFunctions.push featureDisplay
# Comment.
buttons = d3.selectAll(".page_indicator")
buttonColor = buttons.style "background-color"

buttons.on d3plus.client.pointer.click, ->
  featuredPage = parseFloat(@id.split("_")[1])
  featureDisplay(featuredPage)

dataviva.tooltip d3.selectAll(".page_indicator")

d3.select("#featured").on d3plus.client.pointer.over, ->
  clearInterval(autoPagination)
  d3.select(this).on d3plus.client.pointer.over, null

autoPagination = setInterval( ->
  featuredPage++
  featureDisplay(featuredPage)
, 6000)

colorLevels = ["primary", "secondary", "tertiary"]
featuredColors = {}

d3.selectAll(".featured_link").each (d, i) ->
  child     = d3.select(this).select(".paralax")
  colors = []
  for level in colorLevels
    color = child.attr("data-"+level)
    colors.push color if color
  featuredColors[i] = {}
  for c in colors
    if d3.hsl(c).l >= 0.9
      featuredColors[i].light = c
      break
  for c in colors
    if d3.hsl(c).l <= 0.6
      featuredColors[i].dark = c
      break
  featuredColors[i].background = colors[0]
  featuredColors[i].accent = colors[1]
  light = featuredColors[i].light
  if light
    d3.select(this).selectAll("h1, h4").style "color", light

featureDisplay(featuredPage)

addLi = (page, item) ->

  page.append("li").append("a")
    .attr("class", "poster")
    .attr("href", item.url)
    .style("background-image", "url('" + item.image.url + "')")
    .append("h4").attr("class", "title").text(item.title)
      .style("background-color", item.palette[0])
      .style("color", item.palette[1])

addNodes = (page, list) ->
  for i of list
    item = list[i]
    addLi page, item

loadMore = (parentNode, page, callback) ->
  offset = page.selectAll("li").size()
  params = page.attr("data-parameters")
  url = params + "&offset=" + offset
  d3.json url, (error, json) ->
    if error
      return console.warn(error)
    else if not json or json.length is 0
      return console.log("No more data available")
    d3.select(parentNode).select("a.next").classed "disabled", false
    result = addNodes(page, json)
    callback result if callback
    result

onArrowClick = (d) ->

  page_el = d3.select(@parentNode).select(".page")
  transform = page_el.style(prefix + "transform")
  if transform is "none"
    current_x = 0
  else
    current_x = d3.transform(transform).translate[0]
  poster_w = parseInt(d3.select(".poster").style("width"))
  poster_w += parseInt(d3.select(".poster").style("margin-left")) * 2
  container_w = parseInt(d3.select(".page").style("width"))
  if d3.select(this).attr("class").indexOf("next") > -1
    d3.select(@parentNode).select("a.prev").classed "disabled", false
    next_x = current_x - container_w
    max_left = (page_el.selectAll("li").size() * poster_w) * -1
    max_left += container_w
    next_x = (if next_x < max_left then max_left else next_x)
    next_x = (if next_x > 0 then 0 else next_x)
    if next_x is max_left
      loadMore @parentNode, page_el
      d3.select(@parentNode).select("a.next").classed "disabled", true
  else
    d3.select(@parentNode).select("a.next").classed "disabled", false
    next_x = current_x + container_w
    next_x = (if next_x > 0 then 0 else next_x)
    d3.select(@parentNode).select("a.prev")
      .classed "disabled", true if next_x is 0
  page_el.style prefix + "transform", "translateX(" + (next_x) + "px)"

addCarousel = (title, url) ->
  main = document.getElementById("caros")
  section = document.createElement("section")
  section.className = "list"
  div = document.createElement("div")
  h2 = document.createElement("h2")
  h2.innerText = title
  div.appendChild h2
  aprev = document.createElement("a")
  aprev.className = "prev disabled"
  anext = document.createElement("a")
  anext.className = "next"
  section.appendChild div
  section.appendChild aprev
  section.appendChild anext
  divscroll = document.createElement("div")
  divscroll.className = "scroller"
  ul = document.createElement("ul")
  ul.setAttribute "data-parameters", url
  ul.className = "page"
  divscroll.appendChild ul
  section.appendChild divscroll
  loadMore section, d3.select(ul), (results) ->
    if results.length > 0
      main.insertBefore section, main.firstChild
      d3.selectAll("a.next, a.prev").on "click", onArrowClick

addCarousel("Recently Viewed Profiles", "/stats/recent/pages?limit=10&sort=des")
addCarousel("Suggested Profiles", "/stats/suggested/pages?limit=10")

d3.selectAll("a.next, a.prev").on d3plus.client.pointer.click, onArrowClick
