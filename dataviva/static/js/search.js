(function() {
  var WARNING, attr_types, attrs, availBuilds, availTypes, builds, delay, firstLoad, loadAttrs, lockedAttrs, profiles, runSearch, threshold, timeoutID, topK, type2attrs, type2fuse, type2possibleids, updateSuggestion, weights,
    __indexOf = [].indexOf || function(item) { for (var i = 0, l = this.length; i < l; i++) { if (i in this && this[i] === item) return i; } return -1; };

  WARNING = "This file was compiled from coffeescript. Do not edit the .js file!";

  firstLoad = true;

  updateSuggestion = false;

  attr_types = ["bra", "hs", "wld", "cnae", "cbo"];

  threshold = 0.3;

  delay = 100;

  topK = 15;

  lockedAttrs = [];

  timeoutID = null;

  attrs = [];

  weights = {};

  type2fuse = {};

  type2attrs = {};

  type2possibleids = {};

  builds = [];

  profiles = [];

  availBuilds = [];

  availTypes = {};

  dataviva.old_search = function(opts) {
    var loading;
    loading = dataviva.loading(opts.input).text("Loading Attributes").color(d3plus.color.text(d3.select(opts.input).style("background-color")));
    return loadAttrs(opts);
  };

  loadAttrs = function(opts) {
    var data, q, stored, t, url, _i, _len;
    q = queue();
    for (_i = 0, _len = attr_types.length; _i < _len; _i++) {
      t = attr_types[_i];
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
        weight = weights[type];
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
          attr.normName = attr.id + " " + dataviva.removeAccents(attr.name);
          attrs.push(attr);
        }
        type2fuse[type] = new Fuse(subattrs, {
          keys: ['normName'],
          includeScore: true,
          threshold: threshold
        });
      }
      return runSearch(opts);
    });
  };

  runSearch = function(opts) {
    var a, attr, buildSuggestions, builder, createInput, fuse, generalBuild, getAvailableBuildsAndTypes, getIndices, getPossibleIds, list, loadBuild, lockedBuild, profileSuggestions, removeBuild, removeValue, replaceStart, searchBox, selectBuild, source, t, _i, _len, _ref;
    lockedBuild = opts.build;
    if (lockedBuild) {
      _ref = lockedBuild.filter_ids;
      for (t in _ref) {
        list = _ref[t];
        for (_i = 0, _len = list.length; _i < _len; _i++) {
          a = list[_i];
          attr = type2attrs[t].filter(function(d) {
            return d[t + "_id"] === a;
          });
          lockedAttrs.push(attr[0]);
        }
      }
    }
    removeBuild = d3.select(opts.input).html("").append("span").attr("id", "removeBuild").on(d3plus.client.pointer.click, function() {
      lockedBuild = false;
      return updateSuggestion();
    });
    searchBox = d3.select(opts.input).append("span").attr("id", "searchItems");
    loadBuild = d3.select(opts.input).append("a").attr("id", "loadBuild").attr("class", "decision arrow inline button").html("Go");
    if (opts.profiles) {
      builder = dataviva.dict.builder;
      d3.select(opts.input).append("a").attr("class", "advanced").attr("href", "/builder/").html(builder + " <i class='fa fa-angle-double-right'></i>");
    }
    if (opts.builds) {
      buildSuggestions = d3.select(opts.results).append("div").attr("id", "buildSuggestions");
    }
    if (opts.profiles) {
      profileSuggestions = d3.select(opts.results).append("div").attr("id", "profileSuggestions");
      profileSuggestions.append("h2").text(dataviva.dict.profile_plural);
    }
    fuse = new Fuse(attrs, {
      keys: ['normName'],
      includeScore: true,
      threshold: threshold
    });
    getIndices = function(pattern, str) {
      var idx, indices, searchStrLen, startIndex;
      startIndex = 0;
      searchStrLen = pattern.length;
      indices = [];
      while ((idx = str.indexOf(pattern, startIndex)) > -1) {
        indices.push(idx);
        startIndex = idx + searchStrLen;
      }
      return indices;
    };
    replaceStart = function(orig, pattern, newPattern, start) {
      return orig.substr(0, start) + orig.substr(start).replace(pattern, newPattern);
    };
    removeValue = function(array, value) {
      var index;
      index = array.indexOf(value);
      if (index > -1) {
        array.splice(index, 1);
      }
      return index;
    };
    getPossibleIds = function(filterType, index, build, cb) {
      var dataurl, dataurls, filterPart, filtered, hasShow, idxs, lockedTypes, q, queries, query, str, _j, _k, _len1, _len2;
      lockedTypes = {};
      for (_j = 0, _len1 = lockedAttrs.length; _j < _len1; _j++) {
        attr = lockedAttrs[_j];
        lockedTypes[attr.type] = true;
      }
      if ((build == null) && filterType in lockedTypes) {
        cb(null, null);
        return;
      }
      if (filterType in type2possibleids) {
        cb(null, type2possibleids[filterType]);
        return;
      }
      dataurls = [].filter(function(url) {
        return (build == null) || url.indexOf('/' + build.dataset + '/') === 0;
      });
      filterPart = '<' + filterType + '>';
      queries = (function() {
        var _k, _l, _len2, _len3, _results;
        _results = [];
        for (_k = 0, _len2 = dataurls.length; _k < _len2; _k++) {
          dataurl = dataurls[_k];
          hasShow = false;
          if (index != null) {
            idxs = getIndices(filterPart, dataurl);
            if (index < idxs.length) {
              hasShow = true;
              dataurl = replaceStart(dataurl, filterPart, 'show', idxs[index]);
            }
          }
          filtered = false;
          for (_l = 0, _len3 = lockedAttrs.length; _l < _len3; _l++) {
            attr = lockedAttrs[_l];
            str = '<' + attr.type + '>';
            if (dataurl.indexOf(str) >= 0) {
              dataurl = dataurl.replace(str, attr.id);
              filtered = true;
            }
          }
          if (!filtered) {
            continue;
          }
          if (!hasShow) {
            if (dataurl.indexOf(filterPart) < 0) {
              continue;
            }
            dataurl = dataurl.replace(filterPart, 'show');
          }
          _results.push(dataurl.replace(/<(.*?)>/g, 'all'));
        }
        return _results;
      })();
      if (queries.length === 0) {
        cb(null, null);
        return;
      }
      q = queue();
      for (_k = 0, _len2 = queries.length; _k < _len2; _k++) {
        query = queries[_k];
        console.log('executing query for', filterType, query);
        q.defer(d3.json, query);
      }
      return q.awaitAll(function(error, results) {
        var id, possibleIds, result, weight, _l, _len3, _len4, _m, _ref1;
        if (error) {
          console.log(error);
          cb(null, null);
          return;
        }
        possibleIds = {};
        for (_l = 0, _len3 = results.length; _l < _len3; _l++) {
          result = results[_l];
          result = result.data;
          for (_m = 0, _len4 = result.length; _m < _len4; _m++) {
            _ref1 = result[_m], id = _ref1[0], weight = _ref1[1];
            possibleIds[id] = true;
          }
        }
        type2possibleids[filterType] = possibleIds;
        return cb(null, possibleIds);
      });
    };
    getAvailableBuildsAndTypes = function() {
      var b, build, filters, idx, includeBuild, type, _j, _k, _l, _len1, _len2, _len3;
      b = [];
      t = {};
      for (_j = 0, _len1 = builds.length; _j < _len1; _j++) {
        build = builds[_j];
        filters = build.filter_types.slice(0);
        includeBuild = true;
        for (_k = 0, _len2 = lockedAttrs.length; _k < _len2; _k++) {
          attr = lockedAttrs[_k];
          idx = removeValue(filters, attr.type);
          includeBuild = includeBuild && idx >= 0;
        }
        if (includeBuild) {
          b.push(build);
          for (_l = 0, _len3 = filters.length; _l < _len3; _l++) {
            type = filters[_l];
            t[type] = true;
          }
        }
      }
      return [b, t];
    };
    createInput = function(input, attr, type) {
      var bgColor, inner, placeholder;
      placeholder = type ? dataviva.dict[type] : dataviva.dict.search;
      inner = input.append("input").attr("type", "searchText").classed({
        typeahead: true
      }).attr("placeholder", placeholder).on("focus", function() {
        return d3.select(this).attr("placeholder", "");
      }).on("blur", function() {
        return d3.select(this).attr("placeholder", placeholder);
      });
      if (attr != null) {
        t = attr.type;
        if (t !== "bra" && (t !== "wld" || attr[t + "_id"].length === 2)) {
          bgColor = attr.color;
        } else {
          bgColor = "none";
        }
        input.append("span").attr("class", "icon").style("background-image", "url(" + attr.icon + ")").style("background-color", bgColor);
        input.append("span").attr("class", "close");
      }
      $(inner.node()).typeahead({
        minLength: 0,
        highlight: true,
        hint: true,
        autoselect: true
      }, {
        name: 'search-freely',
        displayKey: function(row) {
          return row.attr.name;
        },
        source: (function(attr) {
          return function(text, cb) {
            clearTimeout(timeoutID);
            return timeoutID = setTimeout(function() {
              t = attr != null ? attr.type : type;
              return source(text, t, null, lockedBuild, cb);
            }, delay);
          };
        })(attr),
        templates: {
          empty: '<span class="suggestion">No matches found.</span>',
          suggestion: function(row) {
            var core, prefix, suffix;
            prefix = '';
            suffix = '';
            if ((row.first != null) && !type) {
              prefix = '<span class="suggestion-header">';
              prefix += dataviva.dict[row.attr.type + "_plural"] + '</span>';
            }
            if ((row.left != null) && !type) {
              suffix = '<span class="suggestion-footer">';
              suffix += '... and ' + row.left + ' more</span>';
            }
            core = "<span class='suggestion'>" + row.attr.name + "</span>";
            return prefix + core + suffix;
          }
        }
      }).focus(function() {
        var val;
        val = $(this).typeahead('val');
        if (val === '') {
          $(this).typeahead('val', '.');
          return $(this).typeahead('val', '');
        }
      }).on('typeahead:selected typeahead:autocompleted', function(ev, row) {
        lockedAttrs.push(row.attr);
        type2possibleids = {};
        return updateSuggestion();
      });
      if (attr != null) {
        $(inner.node()).val(attr.name);
        inner.attr('disabled', true);
        return input.on(d3plus.client.pointer.click, (function(attr) {
          return function() {
            removeValue(lockedAttrs, attr);
            type2possibleids = {};
            return updateSuggestion();
          };
        })(attr));
      }
    };
    generalBuild = function() {
      var input, _j, _len1;
      removeBuild.style("display", "none");
      loadBuild.style('display', "none");
      searchBox.html('');
      if (d3.keys(availTypes).length > 0) {
        attrs = lockedAttrs.concat(null);
      } else {
        attrs = lockedAttrs;
      }
      for (_j = 0, _len1 = attrs.length; _j < _len1; _j++) {
        attr = attrs[_j];
        input = searchBox.append("span").attr("class", "lockedAttr");
        createInput(input, attr);
      }
      if (!firstLoad) {
        $(document).find('input:enabled.tt-input').first().focus();
      }
      return firstLoad = false;
    };
    selectBuild = function(build) {
      var input, span, title, type, _j, _k, _len1, _len2, _ref1, _ref2;
      lockedBuild = build;
      window.scrollTo(0, 0);
      d3.select(opts.input).node().parentNode.scrollTop = 0;
      title = build.stem;
      _ref1 = build.filter_types;
      for (_j = 0, _len1 = _ref1.length; _j < _len1; _j++) {
        type = _ref1[_j];
        span = "<span data-type='" + type + "'></span>";
        title = title.replace(new RegExp("\<" + type + "(.*)\>", "gm"), span);
      }
      searchBox.html(title);
      _ref2 = build.filter_types;
      for (_k = 0, _len2 = _ref2.length; _k < _len2; _k++) {
        type = _ref2[_k];
        attrs = (function() {
          var _l, _len3, _results;
          _results = [];
          for (_l = 0, _len3 = lockedAttrs.length; _l < _len3; _l++) {
            attr = lockedAttrs[_l];
            if (attr.type === type) {
              _results.push(attr);
            }
          }
          return _results;
        })();
        input = searchBox.selectAll("span[data-type='" + type + "']").attr("class", "lockedAttr").each(function(d, i) {
          attr = i < attrs.length ? attrs[i] : void 0;
          return createInput(d3.select(this), attr, type);
        });
      }
      removeBuild.style('display', "inline-block");
      if (lockedBuild.completion === 1) {
        loadBuild.style('display', "inline-block").attr("href", opts.callback ? null : lockedBuild.url).on(d3plus.client.pointer.click, function() {
          if (opts.callback) {
            return dataviva[opts.callback](lockedBuild);
          }
        });
      } else {
        loadBuild.style("display", "none");
      }
      return $(document).find('input:enabled.tt-input').first().focus();
    };
    updateSuggestion = function() {
      var i, jsonPost, _j, _len1;
      jsonPost = "";
      for (i = _j = 0, _len1 = lockedAttrs.length; _j < _len1; i = ++_j) {
        a = lockedAttrs[i];
        jsonPost += i === 0 ? "?" : "&";
        jsonPost += a.type + "=" + a[a.type + "_id"];
      }
      return d3.json("/search/results/" + jsonPost, function(error, data) {
        var dataBuilds, defaultImage, profileButtons, profileEnter, sections, _ref1;
        builds = data.builds;
        profiles = data.profiles;
        _ref1 = getAvailableBuildsAndTypes(), availBuilds = _ref1[0], availTypes = _ref1[1];
        if (opts.profiles) {
          defaultImage = "/static/img/bgs/triangles.png";
          profileButtons = profileSuggestions.selectAll(".poster").data(profiles, function(d) {
            return d.stem;
          });
          profileEnter = profileButtons.enter().append("div").attr("class", "poster");
          profileEnter.append("span").attr("class", "title").append("h4");
          profileButtons.order().style("background-image", function(d) {
            var img, sameStem, sub, subData;
            if (lockedBuild) {
              sameStem = lockedBuild.stem === d.stem;
              if (sameStem) {
                lockedBuild = d;
              }
            }
            subData = d.subtitle ? [d.subtitle] : [];
            d3.select(this).select(".title h4").text(d.title);
            sub = d3.select(this).select(".title").selectAll("sub").data(subData);
            sub.enter().append("sub");
            sub.text(String);
            sub.exit().remove();
            if (d.image && d.completion === 1) {
              img = d.image.url;
            } else {
              img = defaultImage;
            }
            return "url(" + img + ")";
          }).on('click', function(d) {
            return selectBuild(d);
          });
          profileButtons.exit().remove();
        }
        if (opts.builds) {
          dataBuilds = availBuilds.reduce(function(obj, build) {
            var dataset;
            dataset = build.data_type;
            if (!(dataset in obj)) {
              obj[dataset] = [];
            }
            obj[dataset].push(build);
            return obj;
          }, {});
          sections = buildSuggestions.selectAll("div").data(d3.keys(dataBuilds), function(d) {
            return d;
          });
          sections.enter().append("div").append("h2").text(function(d) {
            return dataviva.dict[d + "_search"];
          });
          sections.exit().remove();
          sections.each(function(d) {
            var buildButtons, sectionBuilds;
            sectionBuilds = dataBuilds[d];
            buildButtons = d3.select(this).selectAll(".searchBuild").data(sectionBuilds, function(d) {
              return d.app_type + "_" + d.stem;
            });
            buildButtons.enter().append("div");
            return buildButtons.order().attr('class', function(d) {
              var active, sameStem;
              if (lockedBuild) {
                sameStem = lockedBuild.stem === d.stem;
                if (lockedBuild.app_type === d.app_type && sameStem) {
                  lockedBuild = d;
                }
              }
              active = d.completion === 1 ? " active" : "";
              return 'searchBuild decision icon ' + d.app_type + active;
            }).html(function(d) {
              return d.title;
            }).on('click', function(d) {
              return selectBuild(d);
            });
          });
        }
        if (lockedBuild) {
          return selectBuild(lockedBuild);
        } else {
          return generalBuild();
        }
      });
    };
    source = function(text, specificType, index, build, cb) {
      var attrResults, attrtype, globalid, id2attrScore, ncompletedcalls, q, score, types, word, wordResults, words, _fn, _j, _k, _l, _len1, _len2, _len3, _len4, _len5, _m, _n, _ref1, _ref2;
      cb([
        {
          attr: {
            name: "Loading possible values..."
          }
        }
      ]);
      _ref1 = getAvailableBuildsAndTypes(), availBuilds = _ref1[0], availTypes = _ref1[1];
      text = dataviva.removeAccents(text.trim());
      types = specificType != null ? [specificType] : attr_types;
      types = types.filter(function(type) {
        return type in availTypes;
      });
      if (text.length === 0) {
        attrResults = [];
        ncompletedcalls = 0;
        _fn = function(attrtype) {
          return getPossibleIds(attrtype, index, build, function(err, ids) {
            var i, nrows, row, topattr, _k, _len2, _ref2;
            attrs = type2attrs[attrtype].filter(function(attr) {
              return (ids == null) || attr.id in ids;
            });
            if (ids != null) {
              console.log(attrtype, Object.keys(ids).length);
            }
            nrows = Math.ceil(topK / types.length);
            _ref2 = attrs.slice(0, nrows);
            for (i = _k = 0, _len2 = _ref2.length; _k < _len2; i = ++_k) {
              topattr = _ref2[i];
              row = {
                attr: topattr
              };
              if (types.length > 1 && i === 0) {
                row.first = true;
              }
              if (i === nrows - 1) {
                row.left = attrs.length - nrows;
              }
              attrResults.push(row);
            }
            ncompletedcalls += 1;
            if (ncompletedcalls === types.length || attrs.length > 0) {
              return cb(attrResults);
            }
          });
        };
        for (_j = 0, _len1 = types.length; _j < _len1; _j++) {
          attrtype = types[_j];
          _fn(attrtype);
        }
        return;
      }
      q = queue();
      for (_k = 0, _len2 = types.length; _k < _len2; _k++) {
        attrtype = types[_k];
        q.defer(getPossibleIds, attrtype, index, build);
      }
      words = text.split(/[ ,]+/);
      id2attrScore = {};
      for (_l = 0, _len3 = words.length; _l < _len3; _l++) {
        word = words[_l];
        for (_m = 0, _len4 = types.length; _m < _len4; _m++) {
          attrtype = types[_m];
          wordResults = type2fuse[attrtype].search(word);
          for (_n = 0, _len5 = wordResults.length; _n < _len5; _n++) {
            _ref2 = wordResults[_n], attr = _ref2.item, score = _ref2.score;
            globalid = attr.type + "|" + attr.id;
            if (!(globalid in id2attrScore)) {
              id2attrScore[globalid] = [attr, 0];
            }
            id2attrScore[globalid][1] += 1 - score;
          }
        }
      }
      return q.awaitAll(function(error, results) {
        var i, idx, nrows, row, scoreAttr, topattr, _len6, _o, _ref3, _ref4, _ref5;
        scoreAttr = [];
        for (globalid in id2attrScore) {
          _ref3 = id2attrScore[globalid], attr = _ref3[0], score = _ref3[1];
          idx = types.indexOf(attr.type);
          if ((results[idx] == null) || attr.id in results[idx]) {
            scoreAttr.push([score, attr]);
          }
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
        nrows = topK;
        attrResults = [];
        _ref4 = scoreAttr.slice(0, nrows);
        for (i = _o = 0, _len6 = _ref4.length; _o < _len6; i = ++_o) {
          _ref5 = _ref4[i], score = _ref5[0], topattr = _ref5[1];
          row = {
            attr: topattr
          };
          if (i === nrows - 1) {
            row.left = scoreAttr.length - nrows;
          }
          attrResults.push(row);
        }
        return cb(attrResults);
      });
    };
    return updateSuggestion();
  };

}).call(this);
