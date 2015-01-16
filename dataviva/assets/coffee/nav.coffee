WARNING = "This file was compiled from coffeescript. Do not edit the .js file!"

dataviva.search d3.select("#navSearch")

# header        = d3.select("header")
# padding       = false
# domain        = false
# shadowOpacity = false
# logoScale     = false
# logoPadding   = false
# linkPadding   = false
# iconScale     = false
# oldWidth      = false
# shadow        = header.style("box-shadow")
#
# sizeChange = (animate) ->
#   change = oldWidth is false or oldWidth > 980 and window.innerWidth <= 980 or
#            oldWidth <= 980 and window.innerWidth > 980
#   subnav = header.select(".subnav")
#   unless subnav.empty()
#     x = header.select("header a.link.active").node().offsetLeft
#     x += header.select("header a.link.active").node().offsetWidth / 2
#     subnav.select(".triangle").style "left", x + "px"
#     subnav = parseFloat(subnav.node().offsetHeight, 10)
#   else
#     subnav = 0
#   if change
#     height = (if window.innerWidth <= 980 then 35 else 80)
#     logoHeight = header.select("#logo").node().offsetHeight
#     padding = (if window.innerWidth <= 980 then 0 else 10)
#     d3.select("main").style "margin-top", (height + subnav) + "px"
#     minHeight = 30
#     domain = [
#       0
#       height - minHeight
#     ]
#     shadowOpacity = d3.scale.linear().domain(domain).range([
#       0
#       shadow.split(",")[3]
#     ])
#     logoScale = d3.scale.linear().domain(domain).rangeRound([
#       100
#       ((minHeight) / logoHeight) * 100
#     ])
#     logoPadding = d3.scale.linear().domain(domain).rangeRound([
#       padding
#       0
#     ])
#     linkPadding = d3.scale.linear().domain(domain).rangeRound([
#       padding * 2
#       padding
#     ])
#     iconScale = d3.scale.linear().domain(domain).range([
#       1
#       0
#     ])
#     oldWidth = window.innerWidth
#     animate = true if animate is undefined
#     resizeNav animate
#   return
#
# resizeNav = (animate, scroll) ->
#   open = d3.select("#sideMenu").style("left") is "0px"
#   if open and window.innerWidth > 980
#     d3.select("#hamburger").selectAll("span").classed "clicked", false
#     d3.select("#sideMenu").classed "open", false
#     d3.select("body").classed "offset", false
#   if typeof scroll isnt "number"
#     scroll = d3.max([
#       0
#       d3.min([
#         domain[1]
#         window.scrollY
#       ])
#     ])
#
#   scroll = 0 if window.innerHeight >= document.body.offsetHeight or
#                 window.innerWidth <= 980
#
#   style = (header) ->
#     s = shadow.split(",")
#     s[3] = shadowOpacity(scroll)
#     header
#       .style "top", "-" + scroll + "px"
#       .style "box-shadow", s.join(",")
#       .select "#logo"
#         .style "background-size", "auto " + logoScale(scroll) + "%"
#         .style "margin-bottom", logoPadding(scroll) + "px"
#         .style "margin-top", padding + padding - logoPadding(scroll) + "px"
#
#     header.selectAll "a.link, #nav_controls"
#       .style "margin-bottom", linkPadding(scroll) + "px"
#       .style "margin-top", padding * 4 - linkPadding(scroll) + "px"
#       .select "#language"
#         .style "opacity", iconScale(scroll)
#
#     header.selectAll "a.link div.icon"
#       .style d3plus.client.prefix() + "transform", "scale(" + iconScale(scroll) + ")"
#
#   if animate is true
#     header.transition().duration(timing).call style
#   else if typeof animate is "number"
#     header.transition().duration(animate).call style
#   else
#     header.call style
#
# snapFunctions.push resizeNav
# resizeFunctions.push sizeChange
# scrollFunctions.push resizeNav
# sizeChange false
#
# header
#   .on d3plus.client.pointer.over, -> resizeNav 100, 0
#   .on d3plus.client.pointer.out, -> resizeNav 100

# d3plus.form()
#   .data "#language_select"
#   .focus "{{ g.locale }}", (l) ->
#     if l isnt dataviva.language
#       window.location = "/set_lang/" + l + "/?next=" + window.location.pathname
#   .type "drop"
#   .font
#     family: "Source Sans Pro"
#     size: 10
#     weight: 400
#   .ui
#     padding: 4
#     margin: 0
#     color:
#       secondary: "#aaa"
#   .width 100
#   .draw()

# unless d3.select("div#account_tooltip").empty()
#
#   show_toggle = ->
#     d3.select "#account"
#       .attr "class", "active"
#     d3.select "#d3plus_tooltip_id_account"
#       .style "left", x
#       .style "display", "block"
#
#   hide_toggle = ->
#     d3.select("#account").attr "class", ""
#     d3.select("#d3plus_tooltip_id_account").style "display", "none"
#
#   language_html = d3.select("div#account_tooltip").html()
#   d3.select("div#account_tooltip").remove()
#   diff_screen = ((window.outerWidth - parseInt(d3.select("#header").style("width").replace("px", ""))) / 2)
#   acct = d3.select("#account").node()
#   w = acct.offsetWidth
#   h = acct.offsetHeight
#   x = (acct.offsetLeft + (w / 2) + diff_screen)
#   y = acct.offsetTop + h
#
#   d3plus.tooltip.create
#     id: "account"
#     x: x
#     y: y
#     arrow: true
#     align: "bottom center"
#     mouseevents: true
#     html: language_html
#     width: "auto"
#
#   d3.select("#d3plus_tooltip_id_account")
#     .style("display", "none")
#     .on d3plus.client.pointer.click, -> d3.event.stopPropagation()
#
#   d3.select("#account").on d3plus.client.pointer.click, ->
#     if @className.indexOf("active") < 0
#       show_toggle()
#     else
#       hide_toggle()
#     d3.event.stopPropagation()
#     return
#
#   d3.select("body").on d3plus.client.pointer.click, ->
#     hide_toggle()
#     return
#
# else
#   d3.select("#account").on d3plus.client.pointer.click, -> login()

# d3.selectAll("a.link.disable").on d3plus.client.pointer.click, ->
#   d3.event.preventDefault()
#   dataviva.flash @innerHTML + " is currently being redesigned, we will announce when it is ready."

# d3.select("#hamburger").on d3plus.client.pointer.click, ->
#   closed = d3.select("#sideMenu").style("left") isnt "0px"
#   d3.select(this).selectAll("span").classed "clicked", closed
#   d3.select("#sideMenu").classed "open", closed
#   d3.select("body").classed "offset", closed
