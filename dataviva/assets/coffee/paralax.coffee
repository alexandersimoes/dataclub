WARNING = "This file was compiled from coffeescript. Do not edit the .js file!"

easing = (a, b) -> (t) -> (b - a) * t + a

transition = (object, animate, styles) ->
  if animate
    object.transition().duration(timing).style styles
  else
    object.style styles

paralax = (animate) ->
  animate = undefined if animate isnt true
  d3.selectAll("section.paralax").each (d, i) ->

    bg     = d3.select(this).select("div.background")
    top    = @offsetTop
    domain = [top - window.innerHeight, top + @offsetHeight]
    scale  = d3.scale.linear()
      .domain domain
      .interpolate easing

    updateImage = () ->
      image = object.node().getBoundingClientRect()
      container = object.node().parentNode.getBoundingClientRect()
      i_aspect = image.width/image.height
      c_aspect = container.width/container.height
      if c_aspect > i_aspect
        object.style("width", "105%").style("height", "auto")
      else
        object.style("height", "105%").style("width", "auto")
      height = object.node().getBoundingClientRect().height
      scale.range [-(height - container.height - 10), 0]
      styles = top: scale(window.scrollY) + "px"
      transition object, animate, styles

    if bg.empty()
      scale.range [100, 0]
      styles = "background-position": "50% " + scale(window.scrollY) + "%"
      transition d3.select(this), animate, styles
    else
      object = bg.select("img")
      if object.node().getBoundingClientRect().height is 0
        object.node().onload = updateImage
      else
        updateImage()

    return

resizeFunctions.push paralax
scrollFunctions.push paralax
paralax()
setTimeout(paralax, 20)
