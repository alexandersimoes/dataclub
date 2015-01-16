(function() {
  var WARNING,
    __indexOf = [].indexOf || function(item) { for (var i = 0, l = this.length; i < l; i++) { if (i in this && this[i] === item) return i; } return -1; };

  WARNING = "This file was compiled from coffeescript. Do not edit the .js file!";

  window.dataviva = {
    "depths": {}
  };

  dataviva.cleanData = function(data, attr, attr_key, group, url) {
    var allowedSC, demo, depths, id_key, returnData, split_key;
    demo = url && url.indexOf("/attrs/d/") >= 0;
    depths = dataviva.depths[attr];
    if (["bra_s", "bra_r", "cnae_s", "cnae_r"].indexOf(attr_key) >= 0) {
      split_key = attr_key.split("_");
      id_key = split_key[0] + "_id_" + split_key[1];
    } else if (demo) {
      id_key = "id";
    } else {
      id_key = attr + "_id";
    }
    returnData = data.data.map(function(d) {
      var dataObj, data_id, depth, _i, _len;
      dataObj = d.reduce(function(obj, value, i) {
        var header;
        header = data.headers[i];
        if (header === "id") {
          header = id_key;
        }
        obj[header] = value;
        return obj;
      }, {});
      if (!demo) {
        data_id = dataObj[id_key];
        d = depths.slice(0, depths.indexOf(data_id.length) + 1);
        for (_i = 0, _len = d.length; _i < _len; _i++) {
          depth = d[_i];
          dataObj[attr + "_" + depth] = data_id.slice(0, depth);
        }
      }
      return dataObj;
    });
    if (attr_key === "course_sc" && !group) {
      allowedSC = ["xx016", "xx017", "xx018", "xx019", "xx020", "xx021", "xx022"];
      returnData = returnData.filter(function(d) {
        return allowedSC.indexOf(d.course_sc_id) < 0;
      });
    }
    if (group) {
      if (demo) {
        returnData = returnData.reduce(function(obj, value) {
          obj[value.id] = value;
          return obj;
        }, {});
      } else {
        returnData = returnData.reduce(function(obj, value) {
          var id, length;
          length = value[id_key].length;
          id = value[id_key].slice(0, length);
          value[attr + "_" + length] = id;
          if (data.weight) {
            delete value[data.weight];
          }
          if (!obj[attr + "_" + length]) {
            obj[attr + "_" + length] = {};
          }
          obj[attr + "_" + length][id] = value;
          return obj;
        }, {});
      }
    }
    return returnData;
  };

  dataviva.flash = function(text) {
    d3.selectAll("#server_message").remove();
    d3.select("header").append("div").attr("id", "server_message").html(text);
    return setTimeout((function() {
      return d3.selectAll("#server_message").transition().duration(600).style("opacity", 0).remove();
    }), 3000);
  };

  dataviva.lightbox = function(content, opts) {
    var height, lightbox, width;
    if (content) {
      if (!opts) {
        opts = {};
      }
      width = opts.width || window.innerWidth - 80;
      height = opts.height || window.innerHeight - 80;
      d3.select("body").append("div").attr("class", "shield").on(d3plus.client.pointer.click, function() {
        return dataviva.lightbox();
      });
      lightbox = d3.select("body").append("div").attr("class", "lightbox").style("width", width + "px").style("height", height + "px").style("left", (window.innerWidth - width) / 2 + "px").style("top", (window.innerHeight - height) / 2 + "px");
      if (typeof content === "function") {
        return content(lightbox);
      } else {
        return lightbox.html(content);
      }
    } else {
      d3.select(".shield").remove();
      return d3.select(".lightbox").remove();
    }
  };

  dataviva.loading = function(parent) {
    var degree, elem, rotate, self, timer;
    self = this;
    this.div = d3.select(parent).append("div").attr("class", "loading");
    this.icon = self.div.append("i").attr("class", "fa fa-certificate fa-spin");
    this.words = self.div.append("div").attr("class", "text");
    this.timing = parseFloat(self.div.style("transition-duration"), 10) * 1000;
    this.show = function(callback) {
      self.div.style("display", "block");
      setTimeout((function() {
        self.div.style("opacity", 1);
        if (callback) {
          setTimeout(callback, self.timing);
        }
      }), 5);
      return self;
    };
    this.hide = function() {
      self.div.style("opacity", 0);
      setTimeout((function() {
        self.div.style("display", "none");
      }), self.timing);
      return self;
    };
    this.text = function(text) {
      self.words.html(text);
      return self;
    };
    this.color = function(color) {
      self.div.style("color", color);
      return self;
    };
    if (!Modernizr.cssanimations) {
      elem = this.icon.node();
      degree = 0;
      timer = void 0;
      rotate = function() {
        if (degree === 360) {
          degree = 0;
        }
        elem.style.msTransform = "rotate(" + degree + "deg)";
        elem.style.transform = "rotate(" + degree + "deg)";
        timer = setTimeout(function() {
          degree = degree + 4;
          rotate();
        }, 20);
      };
      rotate();
    }
    return this;
  };

  dataviva.num_format = function(number, key, vars) {
    var a;
    if (typeof number !== "number") {
      return "-";
    }
    number = d3plus.number.format(number, key, vars);
    if (key in dataviva.affixes && dataviva.restricted_affixes.indexOf(key) < 0) {
      a = dataviva.affixes[key];
      number = a[0] + number + a[1];
    }
    return number;
  };

  dataviva.removeAccents = function(s) {
    var diacritics, i, _i, _ref;
    diacritics = [[/[\300-\306]/g, 'A'], [/[\340-\346]/g, 'a'], [/[\310-\313]/g, 'E'], [/[\350-\353]/g, 'e'], [/[\314-\317]/g, 'I'], [/[\354-\357]/g, 'i'], [/[\322-\330]/g, 'O'], [/[\362-\370]/g, 'o'], [/[\331-\334]/g, 'U'], [/[\371-\374]/g, 'u'], [/[\321]/g, 'N'], [/[\361]/g, 'n'], [/[\307]/g, 'C'], [/[\347]/g, 'c']];
    for (i = _i = 0, _ref = diacritics.length; 0 <= _ref ? _i < _ref : _i > _ref; i = 0 <= _ref ? ++_i : --_i) {
      s = s.replace(diacritics[i][0], diacritics[i][1]);
    }
    return s;
  };

  dataviva.restricted_affixes = ["num_emp", "students", "enrolled", "graduates", "entrants"];

  dataviva.search = function(input, opts) {
    var attrs, datatypes, delay, icon, initSearch, restricted, source, threshold, timeoutID, type2attrs, type2fuse, weights;
    if (!opts) {
      opts = {};
    }
    icon = d3.select(input.node().parentNode).select("i");
    datatypes = opts.attr || ["bra", "hs", "wld", "cnae", "cbo", "course_hedu", "university"];
    if (!(datatypes instanceof Array)) {
      datatypes = [datatypes];
    }
    threshold = 0.3;
    delay = 100;
    timeoutID = null;
    weights = {};
    type2attrs = {};
    type2fuse = {};
    attrs = [];
    restricted = {
      hs: [2, 6],
      cnae: [1, 6],
      cbo: [1, 4]
    };
    input.on("click.load", function() {
      return initSearch();
    });
    initSearch = function() {
      var data, q, stored, t, url, _i, _len;
      input.on("click.load", null);
      q = queue();
      for (_i = 0, _len = datatypes.length; _i < _len; _i++) {
        t = datatypes[_i];
        url = "/attrs/" + t + "/?lang=" + dataviva.language;
        stored = Modernizr.localstorage && url in localStorage && (!(__indexOf.call(dataviva.storage, url) >= 0) || (parseFloat(localStorage[t]) === dataviva.storage[t]));
        if (stored) {
          data = JSON.parse(localStorage[url]);
          dataviva.depths[t] = data.depths;
          weights[t] = data.weight;
          type2attrs[t] = dataviva.cleanData(data, t);
        } else {
          q.defer(function(u, callback) {
            var attr;
            attr = u.split("/")[2];
            return d3.json(u, function(error, data) {
              if (!error) {
                localStorage[attr] = dataviva.storage[attr];
                localStorage[u] = JSON.stringify(data);
                dataviva.depths[attr] = data.depths;
                weights[attr] = data.weight;
                type2attrs[attr] = dataviva.cleanData(data, attr);
              }
              return callback(error, data);
            });
          }, url);
        }
      }
      return q.awaitAll(function() {
        var attr, i, subattrs, type, weight, _j, _len1;
        for (type in type2attrs) {
          subattrs = type2attrs[type];
          if (type in restricted) {
            subattrs = subattrs.filter(function(d) {
              return restricted[type].indexOf(d[type + "_id"].length) >= 0;
            });
          }
          weight = weights[type];
          subattrs = subattrs.filter(function(a) {
            return a[weight];
          });
          subattrs.sort(function(a, b) {
            if (b[type + "_id"].length === a[type + "_id"].length) {
              return b[weight] - a[weight];
            } else {
              return b[type + "_id"].length - a[type + "_id"].length;
            }
          });
          for (i = _j = 0, _len1 = subattrs.length; _j < _len1; i = ++_j) {
            attr = subattrs[i];
            attr.rank = i;
            attr.type = type;
            attr.url = "/profile/" + type + "/" + attr[type + "_id"] + "/";
            attr.id = attr[type + "_id"];
            attr.normName = dataviva.removeAccents(attr.name);
            attrs.push(attr);
          }
          type2fuse[type] = new Fuse(subattrs, {
            keys: ["normName", "id"],
            includeScore: true,
            threshold: threshold
          });
        }
        $(input.node()).typeahead({
          minLength: 1,
          highlight: false,
          hint: true,
          autoselect: true
        }, {
          displayKey: function(row) {
            return row.attr.name;
          },
          source: (function(attr) {
            return function(text, cb) {
              clearTimeout(timeoutID);
              return timeoutID = setTimeout(function() {
                return source(text, cb);
              }, delay);
            };
          })(attr),
          templates: {
            empty: "<div class='tt-suggestion'>No matches found.</div>",
            suggestion: function(row) {
              var color, image, title, w;
              w = weights[row.attr.type];
              t = row.attr.type;
              i = row.attr[t + "_id"];
              image = row.attr.icon;
              color = t === "bra" || (t === "wld" && i.length === 5) ? "transparent" : row.attr.color;
              image = image ? "<span class='icon' style='background-color:" + color + "'><img src='" + image + "'></span>" : "";
              title = "<span class='title'>" + image + row.attr.name + "</span>";
              type = t === "bra" ? dataviva.dict[t + "_" + i.length] : dataviva.dict[t];
              type = "<span class='sub'>" + type + ": " + i + "</span>";
              weight = dataviva.num_format(row.attr[w], w);
              weight = "<span class='sub'>" + dataviva.dict[w] + ": " + weight + "</span>";
              return title + type + weight;
            }
          }
        }).on("typeahead:selected typeahead:autocompleted", function(ev, row) {
          if (row) {
            input.attr("disabled", true);
            icon.attr("class", "fa fa-spinner fa-spin");
            return window.location = row.attr.url;
          }
        });
        return $(input.node().parentNode).find('input:enabled.tt-input').first().focus();
      });
    };
    return source = function(text, cb) {
      var attr, attrResults, attrtype, globalid, i, id2attrScore, idx, nrows, row, score, scoreAttr, topattr, word, wordResults, words, _i, _j, _k, _l, _len, _len1, _len2, _len3, _ref, _ref1, _ref2, _ref3;
      cb([
        {
          attr: {
            name: "Loading..."
          }
        }
      ]);
      words = text.split(/[ ,]+/);
      id2attrScore = {};
      for (_i = 0, _len = words.length; _i < _len; _i++) {
        word = words[_i];
        for (_j = 0, _len1 = datatypes.length; _j < _len1; _j++) {
          attrtype = datatypes[_j];
          wordResults = type2fuse[attrtype].search(word);
          for (_k = 0, _len2 = wordResults.length; _k < _len2; _k++) {
            _ref = wordResults[_k], attr = _ref.item, score = _ref.score;
            globalid = attr.type + "|" + attr.id;
            if (!(globalid in id2attrScore)) {
              id2attrScore[globalid] = [attr, 0];
            }
            id2attrScore[globalid][1] += 1 - score;
          }
        }
      }
      scoreAttr = [];
      for (globalid in id2attrScore) {
        _ref1 = id2attrScore[globalid], attr = _ref1[0], score = _ref1[1];
        idx = datatypes.indexOf(attr.type);
        scoreAttr.push([score, attr]);
      }
      scoreAttr.sort(function(_arg, _arg1) {
        var attrA, attrB, scoreA, scoreB;
        scoreA = _arg[0], attrA = _arg[1];
        scoreB = _arg1[0], attrB = _arg1[1];
        if (scoreA === scoreB) {
          return attrA.rank - attrB.rank;
        }
        return scoreB - scoreA;
      });
      nrows = 5;
      attrResults = [];
      _ref2 = scoreAttr.slice(0, nrows);
      for (i = _l = 0, _len3 = _ref2.length; _l < _len3; i = ++_l) {
        _ref3 = _ref2[i], score = _ref3[0], topattr = _ref3[1];
        row = {
          attr: topattr
        };
        if (i === nrows - 1) {
          row.left = scoreAttr.length - nrows;
        }
        attrResults.push(row);
      }
      return cb(attrResults);
    };
  };

  dataviva.tooltip = function(elems, align) {
    var tooltip;
    if (!elems) {
      elems = d3.selectAll(".alt_tooltip");
    }
    elems.on(d3plus.client.pointer.over, function() {
      return tooltip(this, align);
    }).on(d3plus.client.pointer.out, function() {
      return tooltip(false);
    });
    return tooltip = function(elem, align) {
      var offset, size, t, text;
      d3plus.tooltip.remove("alt_tooltip");
      if (elem) {
        size = elem.getBoundingClientRect();
        text = elem.getAttribute("alt");
        if (text in dataviva.dict) {
          text = dataviva.dict[text];
        }
        if (!align) {
          align = "bottom center";
        }
        t = align.split(" ")[0];
        offset = t === "center" ? size.width / 2 : size.height / 2;
        return d3plus.tooltip.create({
          x: size.left + size.width / 2 + window.scrollX,
          y: size.top + size.height / 2 + window.scrollY,
          offset: offset,
          arrow: true,
          description: text,
          width: "auto",
          id: "alt_tooltip",
          align: align,
          max_width: 400
        });
      }
    };
  };

  dataviva.url = function(build, page) {
    var replace, title, url;
    if (Modernizr.history) {
      if (!page) {
        page = "builder";
      }
      url = build.url.replace("/build/", "/" + page + "/");
      title = build.title;
      replace = window.location.pathname.indexOf(url.split("?")[0]) >= 0;
      if (title) {
        document.title = "DataViva : " + title;
      }
      if (replace) {
        window.history.replaceState({
          prev_request: url
        }, title, url);
      } else {
        window.history.pushState({
          prev_request: url
        }, title, url);
      }
    }
  };

}).call(this);
