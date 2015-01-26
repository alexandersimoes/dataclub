(function() {
  var WARNING, activeSection, colorLevels, mainStyle, notLoaded, profileColor, shadowColor, shadowHSL, shadowStyle, subStyle, testPositions;

  WARNING = "This file was compiled from coffeescript. Do not edit the .js file!";

  colorLevels = ["primary", "secondary", "tertiary"];

  profileColor = {};

  d3.select(".image").each(function() {
    var c, color, colors, level, _i, _j, _k, _len, _len1, _len2;
    colors = [];
    for (_i = 0, _len = colorLevels.length; _i < _len; _i++) {
      level = colorLevels[_i];
      color = d3.select(this).attr("data-" + level);
      if (color) {
        colors.push(color);
      }
    }
    for (_j = 0, _len1 = colors.length; _j < _len1; _j++) {
      c = colors[_j];
      if (d3.hsl(c).l >= 0.9) {
        profileColor.light = c;
        break;
      }
    }
    for (_k = 0, _len2 = colors.length; _k < _len2; _k++) {
      c = colors[_k];
      if (d3.hsl(c).l <= 0.6) {
        profileColor.dark = c;
        break;
      }
    }
    profileColor.background = colors[0];
    profileColor.accent = colors[1];
    if (!profileColor.light) {
      profileColor.light = "#f7f7f7";
    }
    if (!profileColor.dark) {
      profileColor.dark = "#444";
    }
    if (d3.hsl(colors[0]).l > 0.3 && d3.hsl(colors[0]).l < 0.6) {
      return profileColor.labels = colors[0];
    } else if (d3.hsl(colors[1]).l > 0.3 && d3.hsl(colors[1]).l < 0.6) {
      return profileColor.labels = colors[1];
    } else {
      return profileColor.labels = profileColor.dark;
    }
  });

  activeSection = false;

  d3.select("header").style("background-color", profileColor.background).each(function() {
    var text;
    text = d3plus.color.text(profileColor.background);
    if (d3.hsl(text).l > 0.5) {
      if (profileColor.light === profileColor.background || profileColor.light === profileColor.accent) {
        profileColor.link = text;
      } else {
        profileColor.link = profileColor.light;
      }
      d3.select(this).select("#logo").style("color", "white");
    } else {
      if (profileColor.dark === profileColor.background || profileColor.dark === profileColor.accent) {
        profileColor.link = text;
      } else {
        profileColor.link = profileColor.dark;
      }
    }
    d3.select(this).selectAll(".link").style("color", profileColor.link).on(d3plus.client.pointer.over, function() {
      return d3.select(this).style("color", profileColor.accent);
    }).on(d3plus.client.pointer.out, function() {
      return d3.select(this).style("color", profileColor.link);
    });
    d3.select(this).selectAll("li.depth_1").style("color", profileColor.accent).style("background-color", profileColor.background);
    return d3.select(this).selectAll("li.depth_0, li.depth_2, li.depth_3").style("color", profileColor.link).style("background-color", profileColor.background).on(d3plus.client.pointer.over, function() {
      if (this.id !== "link_" + activeSection) {
        return d3.select(this).style("color", profileColor.accent);
      }
    }).on(d3plus.client.pointer.out, function() {
      var color;
      if (this.id !== "link_" + activeSection) {
        color = profileColor.link;
      } else {
        color = d3plus.color.text(profileColor.accent);
      }
      return d3.select(this).style("color", color);
    });
  });

  d3.selectAll("h1").style("color", function(d, i) {
    if (i !== 0) {
      return profileColor.labels;
    }
  });

  d3.select("main").selectAll("h2, h3").style("color", profileColor.labels);

  d3.select(".toggleStats").style("background-color", profileColor.background).style("color", profileColor.accent).on(d3plus.client.pointer.over, function() {
    return d3.select(this).style("background-color", profileColor.background).style("color", profileColor.accent);
  });

  if (d3.hsl(profileColor.background).l > 0.3 && d3.hsl(profileColor.background).l < 0.9) {
    shadowColor = profileColor.background;
  } else if (d3.hsl(profileColor.accent).l > 0.3 && d3.hsl(profileColor.accent).l < 0.9) {
    shadowColor = profileColor.accent;
  } else {
    shadowColor = profileColor.labels;
  }

  shadowHSL = d3.hsl(shadowColor);

  shadowHSL.l = 0.8;

  shadowColor = shadowHSL.toString();

  shadowStyle = "inset 0px -2px 0 ";

  d3.selectAll("p").selectAll("a").style("box-shadow", shadowStyle + shadowColor).on(d3plus.client.pointer.over, function() {
    return d3.select(this).style("color", profileColor.labels).style("box-shadow", "none");
  }).on(d3plus.client.pointer.out, function() {
    return d3.select(this).style("color", "#444").style("box-shadow", shadowStyle + shadowColor);
  });

  mainStyle = function(link) {
    return link.style("background-color", function() {
      if (this.id === "link_" + activeSection) {
        return profileColor.accent;
      } else {
        return profileColor.background;
      }
    }).style("color", function() {
      if (this.id === "link_" + activeSection) {
        return d3plus.color.text(profileColor.accent);
      } else {
        return profileColor.accent;
      }
    });
  };

  subStyle = function(link) {
    return link.style("background-color", function() {
      if (this.id === "link_" + activeSection) {
        return profileColor.accent;
      } else {
        return profileColor.background;
      }
    }).style("color", function() {
      if (this.id === "link_" + activeSection) {
        return d3plus.color.text(profileColor.accent);
      } else {
        return profileColor.link;
      }
    });
  };

  testPositions = function() {
    var activeLink, build, found, i, links, newBuilds, previousLink, rect, top;
    if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight) {
      links = d3.selectAll("a.section_link");
      activeLink = links[0][links.size() - 1].id;
    } else {
      activeLink = false;
      previousLink = false;
      found = false;
      top = 0;
      d3.selectAll("a.section_link").each(function(d, i) {
        var start;
        if (i === 0) {
          start = top;
        }
        if (!found) {
          top = this.getBoundingClientRect().top;
          top += parseFloat(d3.select(this).select("*").style("margin-top"), 10);
          if (top >= -5 && top <= window.innerHeight * 0.25) {
            activeLink = this.id;
            found = true;
          } else if (top > window.innerHeight * 0.25) {
            activeLink = previousLink;
            found = true;
          }
          return previousLink = this.id;
        }
      });
      if (!activeLink && top < 0) {
        links = d3.selectAll("a.section_link");
        activeLink = links[0][links.size() - 1].id;
      }
    }
    if (activeLink !== activeSection) {
      activeSection = activeLink;
      d3.selectAll("li.depth_1").transition().duration(200).call(mainStyle);
      d3.selectAll("li.depth_2, li.depth_3").transition().duration(200).call(subStyle);
    }
    i = notLoaded.length;
    newBuilds = [];
    while (i--) {
      build = notLoaded[i];
      rect = build.container.node().getBoundingClientRect();
      if (rect.top < window.innerHeight && rect.bottom > 0) {
        newBuilds.push(build);
        notLoaded.splice(i, 1);
      }
    }
    return visualization(newBuilds);
  };

  d3.select(".stats").each(function() {
    return d3.select(this).attr("data-height", d3.select(this).style("height")).style("height", "0px").style("visibility", "visible");
  });

  d3.selectAll(".toggleStats").on(d3plus.client.pointer.click, function() {
    var active, height, stats;
    stats = d3.select(".stats");
    active = stats.style("height") === "0px";
    height = active ? stats.attr("data-height") : "0px";
    stats.style("height", height);
    return d3.select(".headlines").classed("active", active);
  });

  d3.selectAll("a.attr").style("color", function(d) {
    var color;
    color = d3.select(this).style("background-color");
    return d3plus.color.text(color);
  });

  notLoaded = [];

  d3.selectAll("div.build").each(function() {
    var build;
    build = dataviva.builds[parseFloat(this.id.split("_")[1])];
    build.container = d3.select(this);
    return notLoaded.push(build);
  });

  document.onscroll = testPositions;

  testPositions();

}).call(this);
