(function() {
  var WARNING, easing, paralax, transition;

  WARNING = "This file was compiled from coffeescript. Do not edit the .js file!";

  easing = function(a, b) {
    return function(t) {
      return (b - a) * t + a;
    };
  };

  transition = function(object, animate, styles) {
    if (animate) {
      return object.transition().duration(timing).style(styles);
    } else {
      return object.style(styles);
    }
  };

  paralax = function(animate) {
    if (animate !== true) {
      animate = void 0;
    }
    return d3.selectAll("section.paralax").each(function(d, i) {
      var bg, domain, object, scale, styles, top, updateImage;
      bg = d3.select(this).select("div.background");
      top = this.offsetTop;
      domain = [top - window.innerHeight, top + this.offsetHeight];
      scale = d3.scale.linear().domain(domain).interpolate(easing);
      updateImage = function() {
        var c_aspect, container, height, i_aspect, image, styles;
        image = object.node().getBoundingClientRect();
        container = object.node().parentNode.getBoundingClientRect();
        i_aspect = image.width / image.height;
        c_aspect = container.width / container.height;
        if (c_aspect > i_aspect) {
          object.style("width", "105%").style("height", "auto");
        } else {
          object.style("height", "105%").style("width", "auto");
        }
        height = object.node().getBoundingClientRect().height;
        scale.range([-(height - container.height - 10), 0]);
        styles = {
          top: scale(window.scrollY) + "px"
        };
        return transition(object, animate, styles);
      };
      if (bg.empty()) {
        scale.range([100, 0]);
        styles = {
          "background-position": "50% " + scale(window.scrollY) + "%"
        };
        transition(d3.select(this), animate, styles);
      } else {
        object = bg.select("img");
        if (object.node().getBoundingClientRect().height === 0) {
          object.node().onload = updateImage;
        } else {
          updateImage();
        }
      }
    });
  };

  resizeFunctions.push(paralax);

  scrollFunctions.push(paralax);

  paralax();

  setTimeout(paralax, 20);

}).call(this);
