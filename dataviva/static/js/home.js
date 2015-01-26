(function() {
  var WARNING, addCarousel, addLi, addNodes, autoPagination, buttonColor, buttons, colorLevels, featureDisplay, featuredColors, featuredPage, loadMore, onArrowClick, prefix;

  WARNING = "This file was compiled from coffeescript. Do not edit the .js file!";

  prefix = d3plus.client.prefix();

  featuredPage = 0;

  featureDisplay = function(page) {
    var color, light, offset, transition;
    transition = page === false ? 0 : timing;
    if (featuredPage >= buttons.size() || featuredPage < 0) {
      featuredPage = 0;
    }
    offset = -featuredPage * window.innerWidth;
    light = featuredColors[featuredPage].light;
    color = light ? light : buttonColor;
    buttons.style("background-color", color).classed("active", false);
    d3.select("#featured_" + featuredPage).classed("active", true);
    return d3.select(".featured_link").transition().duration(transition).style("margin-left", offset + "px");
  };

  resizeFunctions.push(featureDisplay);

  buttons = d3.selectAll(".page_indicator");

  buttonColor = buttons.style("background-color");

  buttons.on(d3plus.client.pointer.click, function() {
    featuredPage = parseFloat(this.id.split("_")[1]);
    return featureDisplay(featuredPage);
  });

  dataviva.tooltip(d3.selectAll(".page_indicator"));

  d3.select("#featured").on(d3plus.client.pointer.over, function() {
    clearInterval(autoPagination);
    return d3.select(this).on(d3plus.client.pointer.over, null);
  });

  autoPagination = setInterval(function() {
    featuredPage++;
    return featureDisplay(featuredPage);
  }, 6000);

  colorLevels = ["primary", "secondary", "tertiary"];

  featuredColors = {};

  d3.selectAll(".featured_link").each(function(d, i) {
    var c, child, color, colors, level, light, _i, _j, _k, _len, _len1, _len2;
    child = d3.select(this).select(".paralax");
    colors = [];
    for (_i = 0, _len = colorLevels.length; _i < _len; _i++) {
      level = colorLevels[_i];
      color = child.attr("data-" + level);
      if (color) {
        colors.push(color);
      }
    }
    featuredColors[i] = {};
    for (_j = 0, _len1 = colors.length; _j < _len1; _j++) {
      c = colors[_j];
      if (d3.hsl(c).l >= 0.9) {
        featuredColors[i].light = c;
        break;
      }
    }
    for (_k = 0, _len2 = colors.length; _k < _len2; _k++) {
      c = colors[_k];
      if (d3.hsl(c).l <= 0.6) {
        featuredColors[i].dark = c;
        break;
      }
    }
    featuredColors[i].background = colors[0];
    featuredColors[i].accent = colors[1];
    light = featuredColors[i].light;
    if (light) {
      return d3.select(this).selectAll("h1, h4").style("color", light);
    }
  });

  featureDisplay(featuredPage);

  addLi = function(page, item) {
    return page.append("li").append("a").attr("class", "poster").attr("href", item.url).style("background-image", "url('" + item.image.url + "')").append("h4").attr("class", "title").text(item.title).style("background-color", item.palette[0]).style("color", item.palette[1]);
  };

  addNodes = function(page, list) {
    var i, item, _results;
    _results = [];
    for (i in list) {
      item = list[i];
      _results.push(addLi(page, item));
    }
    return _results;
  };

  loadMore = function(parentNode, page, callback) {
    var offset, params, url;
    offset = page.selectAll("li").size();
    params = page.attr("data-parameters");
    url = params + "&offset=" + offset;
    return d3.json(url, function(error, json) {
      var result;
      if (error) {
        return console.warn(error);
      } else if (!json || json.length === 0) {
        return console.log("No more data available");
      }
      d3.select(parentNode).select("a.next").classed("disabled", false);
      result = addNodes(page, json);
      if (callback) {
        callback(result);
      }
      return result;
    });
  };

  onArrowClick = function(d) {
    var container_w, current_x, max_left, next_x, page_el, poster_w, transform;
    page_el = d3.select(this.parentNode).select(".page");
    transform = page_el.style(prefix + "transform");
    if (transform === "none") {
      current_x = 0;
    } else {
      current_x = d3.transform(transform).translate[0];
    }
    poster_w = parseInt(d3.select(".poster").style("width"));
    poster_w += parseInt(d3.select(".poster").style("margin-left")) * 2;
    container_w = parseInt(d3.select(".page").style("width"));
    if (d3.select(this).attr("class").indexOf("next") > -1) {
      d3.select(this.parentNode).select("a.prev").classed("disabled", false);
      next_x = current_x - container_w;
      max_left = (page_el.selectAll("li").size() * poster_w) * -1;
      max_left += container_w;
      next_x = (next_x < max_left ? max_left : next_x);
      next_x = (next_x > 0 ? 0 : next_x);
      if (next_x === max_left) {
        loadMore(this.parentNode, page_el);
        d3.select(this.parentNode).select("a.next").classed("disabled", true);
      }
    } else {
      d3.select(this.parentNode).select("a.next").classed("disabled", false);
      next_x = current_x + container_w;
      next_x = (next_x > 0 ? 0 : next_x);
      if (next_x === 0) {
        d3.select(this.parentNode).select("a.prev").classed("disabled", true);
      }
    }
    return page_el.style(prefix + "transform", "translateX(" + next_x + "px)");
  };

  addCarousel = function(title, url) {
    var anext, aprev, div, divscroll, h2, main, section, ul;
    main = document.getElementById("caros");
    section = document.createElement("section");
    section.className = "list";
    div = document.createElement("div");
    h2 = document.createElement("h2");
    h2.innerText = title;
    div.appendChild(h2);
    aprev = document.createElement("a");
    aprev.className = "prev disabled";
    anext = document.createElement("a");
    anext.className = "next";
    section.appendChild(div);
    section.appendChild(aprev);
    section.appendChild(anext);
    divscroll = document.createElement("div");
    divscroll.className = "scroller";
    ul = document.createElement("ul");
    ul.setAttribute("data-parameters", url);
    ul.className = "page";
    divscroll.appendChild(ul);
    section.appendChild(divscroll);
    return loadMore(section, d3.select(ul), function(results) {
      if (results.length > 0) {
        main.insertBefore(section, main.firstChild);
        return d3.selectAll("a.next, a.prev").on("click", onArrowClick);
      }
    });
  };

  addCarousel("Recently Viewed Profiles", "/stats/recent/pages?limit=10&sort=des");

  addCarousel("Suggested Profiles", "/stats/suggested/pages?limit=10");

  d3.selectAll("a.next, a.prev").on(d3plus.client.pointer.click, onArrowClick);

}).call(this);
