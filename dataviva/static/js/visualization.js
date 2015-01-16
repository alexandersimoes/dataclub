(function() {
  var WARNING, checkData, config, configMerge, dataCache, datasetDefault, defaultStyle, demoURL, draw, finish, loadData, locale, page, tickSize, trackedAttrs, urlChecks, visualizations;

  WARNING = "This file was compiled from coffeescript. Do not edit the .js file!";

  visualizations = {};

  dataCache = {};

  trackedAttrs = {};

  page = location.pathname.split("/")[1];

  datasetDefault = {
    rais: "num_emp",
    secex: "export_val",
    ei: "purchase_value",
    sc: "enrolled",
    hedu: "enrolled"
  };

  demoURL = "/attrs/d/?lang=" + dataviva.language;

  locale = dataviva.language === "en" ? "en_US" : "pt_BR";

  tickSize = 15;

  defaultStyle = {
    aggs: {
      wage_avg: function(leaves) {
        var num_emp, wage;
        wage = d3.sum(leaves, function(d) {
          return d.wage;
        });
        num_emp = d3.sum(leaves, function(d) {
          return d.num_emp;
        });
        return wage / num_emp;
      }
    },
    background: "#fafafa",
    font: {
      family: "Oswald",
      weight: 400
    },
    format: {
      locale: locale,
      number: dataviva.num_format,
      text: function(text, key, vars) {
        if (text === "A" && key === "d_id") {
          return "Male";
        }
        if (text === "B" && key === "d_id") {
          return "Female";
        }
        if (key === "threshold") {
          return dataviva.dict[vars.id.value + "_plural"];
        }
        if (text in dataviva.dict) {
          return dataviva.dict[text];
        }
        return d3plus.string.title(text, key, vars);
      }
    },
    legend: {
      size: [24, 24]
    },
    title: {
      font: {
        size: 24
      },
      sub: {
        font: {
          size: tickSize
        }
      },
      total: {
        font: {
          size: tickSize
        }
      }
    },
    x: {
      axis: {
        color: "#ccc",
        font: {
          size: tickSize
        }
      },
      grid: false,
      label: {
        font: {
          size: 24
        }
      },
      ticks: {
        font: {
          size: tickSize
        }
      }
    },
    y: {
      axis: {
        color: "#ccc",
        font: {
          size: tickSize
        }
      },
      grid: false,
      label: {
        font: {
          size: 24
        }
      },
      ticks: {
        font: {
          size: tickSize
        }
      }
    },
    zoom: {
      scroll: false
    }
  };

  configMerge = function(oldParams, newParams) {
    var match, method, preset, ui, value, _i, _len;
    for (method in newParams) {
      if (method in oldParams) {
        preset = oldParams[method];
        value = newParams[method];
        if (method === "ui") {
          for (_i = 0, _len = method.length; _i < _len; _i++) {
            ui = method[_i];
            match = preset.filter(function(m) {
              return m.method === ui.method;
            });
            if (!match.length) {
              oldParams[method].push(ui);
            }
          }
        } else {
          if (!d3plus.object.validate(preset)) {
            preset = {
              value: preset
            };
          }
          if (d3plus.object.validate(value)) {
            preset = d3plus.object.merge(preset, value);
          } else {
            preset.value = value;
          }
          oldParams[method] = preset;
        }
      } else {
        oldParams[method] = newParams[method];
      }
    }
    return oldParams;
  };

  config = function(build) {
    var a, attr, attrs, bras, colorToggle, d, data, defaults, demoAttr, depthToggle, depths, gender, i, iconStyle, key, level, mod, nesting, network, ordering, output, params, size, sizeMethod, sizeToggle, textLabels, times, total, url, _i, _j, _k, _len, _len1, _len2, _ref;
    params = {};
    output = build.display_attr;
    depths = dataviva.depths[output].slice();
    if (depths.length > 2) {
      mod = build.data_type === "ei" && output === "cnae" ? 2 : 1;
      if (output !== "bra") {
        depths = [depths[0], depths[depths.length - mod]];
      } else {
        depths.shift();
        if (build.data_type !== "ei") {
          bras = build.filter_ids.bra.map(function(b) {
            if (b === "sabra") {
              return 0;
            } else {
              return b.length;
            }
          });
          bras = d3.min(bras);
          depths = depths.filter(function(d) {
            return d > bras;
          });
          if (depths.length > 1) {
            depths = [depths[0], depths[depths.length - 1]];
          }
        }
      }
    }
    if (build.network) {
      network = dataCache[build.network];
    }
    if (build.app_type === "tree_map") {
      size = build.config.size || datasetDefault[build.data_type];
      if (dataviva.restricted_affixes.indexOf(size) >= 0 && size in dataviva.affixes) {
        a = dataviva.affixes[size];
        total = {
          prefix: a[0],
          suffix: a[1]
        };
      } else {
        total = true;
      }
      params = {
        data: {
          padding: 0
        },
        labels: {
          align: "start"
        },
        title: {
          total: total
        },
        type: "tree_map"
      };
      if (build.data_type === "ei" && output === "bra") {
        params.depth = 0;
      }
    } else if (build.app_type === "geo_map") {
      params = {
        color: datasetDefault[build.data_type],
        coords: dataCache[build.coords],
        type: "geo_map"
      };
    } else if (build.app_type === "stacked") {
      params = {
        depth: 0,
        shape: {
          interpolate: "monotone"
        },
        timeline: false,
        type: "stacked",
        x: "year",
        y: datasetDefault[build.data_type]
      };
    } else if (build.app_type === "line") {
      params = {
        depth: 0,
        shape: {
          interpolate: "monotone"
        },
        timeline: false,
        type: "line",
        x: "year",
        y: {
          scale: "linear",
          value: datasetDefault[build.data_type]
        }
      };
    } else if (build.app_type === "network") {
      params = {
        active: {
          spotlight: true,
          value: function(d) {
            return d.rca >= 1;
          }
        },
        depth: depths[depths.length - 1],
        edges: network.edges,
        labels: false,
        nodes: network.nodes,
        size: {
          scale: d3.scale.pow().exponent(3 / 8)
        },
        title: {
          sub: "Click to zoom"
        },
        type: "network"
      };
    } else if (build.app_type === "rings") {
      params = {
        depth: depths[depths.length - 1],
        edges: network.edges,
        nodes: network.nodes,
        size: false,
        type: "rings"
      };
    } else if (build.app_type === "scatter") {
      url = build.data_url.split("/");
      url[3] = "all";
      if (build.data_type === "secex") {
        url[2] = 2013;
      }
      url = url.join("/");
      params = {
        active: {
          spotlight: true,
          value: function(d) {
            return d.rca >= 1;
          }
        },
        dataMerge: function(data, extra) {
          var d, ex, _i, _len;
          output = build.display_key + "_id";
          for (_i = 0, _len = data.length; _i < _len; _i++) {
            d = data[_i];
            ex = extra.filter(function(e) {
              return e[output] === d[output];
            })[0];
            if ("pci" in ex) {
              d.pci = ex.pci;
            }
          }
          return data;
        },
        depth: 0,
        extraData: url,
        labels: false,
        type: "scatter",
        x: "distance",
        y: output === "cnae" ? "cbo_diversity_eff" : "pci"
      };
    } else if (build.app_type === "compare") {
      params = {
        labels: false,
        type: "scatter"
      };
    } else if (build.app_type === "occugrid") {
      url = build.data_url.split("/");
      url[3] = "all";
      url = url.join("/");
      params = {
        active: {
          spotlight: true,
          value: "mne_medium"
        },
        dataMerge: function(data, extra) {
          var keys;
          keys = ["mne_micro", "mne_small", "mne_medium", "mne_large", "age_avg", "wage_avg"];
          return data.filter(function(d) {
            var bra;
            bra = extra.filter(function(e) {
              return e.cbo_id === d.cbo_id;
            })[0];
            keys.forEach(function(key) {
              if (key.indexOf("mne") === 0) {
                d[key] = Math.ceil(d[key]);
                d[key + "_bra"] = Math.ceil(bra[key]);
              } else {
                d[key + "_bra"] = bra[key];
              }
            });
            d.importance = bra.importance;
            return bra.importance > 0.25;
          });
        },
        extraData: url,
        id: {
          grouping: false
        },
        size: "importance",
        total: "mne_medium_bra",
        type: "bubbles"
      };
    } else if (build.app_type === "bar") {
      params = {
        order: {
          agg: "max",
          sort: "desc"
        },
        type: "bar",
        y: {
          scale: "linear"
        }
      };
      if (build.demo) {
        params.x = {
          ticks: {
            font: {
              size: 13
            }
          }
        };
      }
    } else if (build.app_type === "pie") {
      params = {
        type: "pie"
      };
    } else if (build.app_type === "box") {
      params = {
        type: {
          mode: [0, 100],
          value: "box"
        }
      };
    }
    nesting = [];
    data = dataCache[build.data_url];
    if (build.demo) {
      attrs = dataCache[demoURL];
      key = output + "_" + depths[depths.length - 1];
      if (build.app_type === "bar") {
        if (build.demo === "gender") {
          if (build.config.order && build.config.order.indexOf(".") > 0) {
            gender = build.config.order.split(".")[1];
          } else {
            gender = "A";
          }
          ordering = gender === "A" ? ["A", "B"] : ["B", "A"];
          data.sort(function(a, b) {
            return ordering.indexOf(a.d_id) - ordering.indexOf(b.d_id);
          });
        } else if (build.demo === "ethnicity") {
          ordering = ["D", "H", "G", "E", "F", "C"];
          data.sort(function(a, b) {
            return ordering.indexOf(a.d_id) - ordering.indexOf(b.d_id);
          });
        }
        build.config.x = output;
      }
      for (_i = 0, _len = data.length; _i < _len; _i++) {
        d = data[_i];
        attr = dataCache[build.attr_url][key][d[key]];
        demoAttr = dataCache[demoURL][d.d_id];
        d[output] = attr.name;
        d.name = demoAttr.name;
      }
      depths = ["d_id"];
      if (build.app_type === "stacked") {
        params.size = {
          threshold: false
        };
        params.y = {
          scale: "share",
          values: params.y
        };
      }
    } else {
      attrs = dataCache[build.attr_url];
    }
    iconStyle = {};
    textLabels = {};
    for (i = _j = 0, _len1 = depths.length; _j < _len1; i = ++_j) {
      d = depths[i];
      level = d !== "d_id" ? output + "_" + d : d;
      if (level.indexOf("bra") === 0 || level === "wld_5") {
        iconStyle[level] = "default";
      } else {
        iconStyle[level] = "knockout";
      }
      textLabels[level] = ["name", level];
      nesting.push(level);
    }
    defaults = {
      attrs: attrs,
      color: "color",
      data: data,
      depth: nesting.length - 1,
      icon: {
        style: iconStyle,
        value: "icon"
      },
      id: nesting,
      size: datasetDefault[build.data_type],
      text: textLabels,
      time: "year"
    };
    defaults.focus = {
      tooltip: ["embed", "builder"].indexOf(page) >= 0 || build.container.classed("lightbox")
    };
    if (build.config.y === "trade_val") {
      defaults.data = defaults.data.reduce(function(arr, d, i) {
        var export_data, import_data;
        export_data = d3plus.util.copy(d);
        export_data.trade_val = export_data.export_val;
        export_data.flow = "export_val";
        export_data.color = "#0b1097";
        delete export_data.export_val;
        delete export_data.import_val;
        import_data = d3plus.util.copy(d);
        import_data.trade_val = import_data.import_val;
        import_data.flow = "import_val";
        import_data.color = "#c8140a";
        delete import_data.export_val;
        delete import_data.import_val;
        arr.push(export_data);
        arr.push(import_data);
        return arr;
      }, []);
      defaults.id.push("flow");
      params.depth = defaults.id.length - 1;
      params.color = "color";
      defaults.text = "flow";
      params.y.label = dataviva.dict["export_import"];
    } else if (build.config.y === "trade_net") {
      _ref = defaults.data;
      for (_k = 0, _len2 = _ref.length; _k < _len2; _k++) {
        d = _ref[_k];
        if (!d.export_val) {
          d.export_val = 0;
        }
        if (!d.import_val) {
          d.import_val = 0;
        }
        d.trade_net = d.export_val - d.import_val;
      }
    }
    if (build.config.split) {
      if (build.config.split === "time") {
        times = {
          morning: "#f7b6d2",
          afternoon: "#ffc41c",
          night: "#2f2f6d",
          full_time: "#105b10"
        };
        defaults.data = defaults.data.reduce(function(arr, d, i) {
          var c2, color, data_obj, t, t2;
          for (t in times) {
            color = times[t];
            data_obj = d3plus.util.copy(d);
            for (t2 in times) {
              c2 = times[t2];
              delete data_obj[t2];
            }
            data_obj.enrolled = d[t];
            data_obj.name = t;
            data_obj.color = color;
            data_obj.icon = "/static/img/icons/time/time_" + t + ".png";
            arr.push(data_obj);
          }
          return arr;
        }, []);
        defaults.id = ["name"];
        defaults.icon.style["name"] = "knockout";
        params.depth = 0;
        if (build.app_type === "stacked") {
          params.size = {
            threshold: false
          };
          params.y = {
            scale: "share",
            values: params.y
          };
        }
      }
      delete build.config.split;
    }
    if (defaults.id[0].indexOf("university") === 0) {
      params.legend = false;
      if ("size" in params) {
        if (d3plus.object.validate(params.size)) {
          params.size.threshold = false;
        } else {
          params.size = {
            threshold: false,
            value: params.size
          };
        }
      } else {
        params.size = {
          threshold: false
        };
      }
    }
    defaults.ui = [];
    if (page !== "profile") {
      depthToggle = defaults.id.reduce(function(arr, n, i) {
        var obj;
        obj = {};
        obj[n] = i;
        arr.push(obj);
        return arr;
      }, []);
      if (build.data_type === "secex") {
        if (output === "hs") {
          colorToggle = ["color", "pci", "opp_gain", "opp_gain_wld", "export_val_growth", "export_val_growth_5", "import_val_growth", "import_val_growth_5"];
        } else {
          colorToggle = ["color", "eci", "hs_diversity", "hs_diversity_eff", "export_val_growth", "export_val_growth_5", "import_val_growth", "import_val_growth_5"];
        }
      } else if (build.data_type === "rais") {
        if (build.app_type === "tree_map") {
          sizeMethod = "size";
          sizeToggle = ["num_emp", "wage", "num_est"];
        } else if (build.app_type === "occugrid") {
          sizeMethod = function(value, viz) {
            if (value === "mne") {
              return viz.size(viz.total()).draw();
            } else {
              return viz.size(value).draw();
            }
          };
          sizeToggle = ["importance", "wage_avg", "wage_avg_bra", "mne"];
        } else {
          sizeMethod = "size";
          sizeToggle = ["num_emp", "wage", "wage_avg", "num_est"];
        }
        if (output === "cnae") {
          colorToggle = ["color", "cbo_diversity", "cbo_diversity_eff", "opp_gain", "wage_growth", "wage_growth_5", "num_emp_growth", "num_emp_growth_5"];
        } else {
          colorToggle = ["color", "wage_growth", "wage_growth_5", "num_emp_growth", "num_emp_growth_5"];
        }
      } else if (build.data_type === "ei") {
        sizeMethod = "size";
        sizeToggle = ["purchase_value", "tax", "icms_tax"];
      } else if (build.data_type === "sc") {
        sizeMethod = "size";
        sizeToggle = ["enrolled", "classes"];
      } else if (build.data_type === "hedu") {
        sizeMethod = "size";
        sizeToggle = ["enrolled", "graduates", "entrants"];
        defaults.ui = [];
      }
      if (sizeToggle && build.app_type === "geo_map") {
        defaults.ui.push({
          label: dataviva.dict.color,
          method: "color",
          value: sizeToggle
        });
      } else {
        if (sizeToggle && build.app_type !== "rings") {
          defaults.ui.push({
            label: dataviva.dict.size,
            method: sizeMethod,
            value: sizeToggle
          });
        }
        if (colorToggle) {
          defaults.ui.push({
            label: dataviva.dict.color,
            method: "color",
            value: colorToggle
          });
        }
      }
      if (build.app_type !== "geo_map" && build.app_type !== "network" && build.app_type !== "rings" && depthToggle.length > 1) {
        defaults.ui.push({
          label: dataviva.dict.depth,
          method: "depth",
          value: depthToggle
        });
      }
      if (build.app_type === "scatter") {
        defaults.ui.push({
          label: dataviva.dict.x,
          method: "x",
          value: ["distance", "opp_gain"]
        });
        if (build.data_type === "rais") {
          defaults.ui.push({
            label: dataviva.dict.y,
            method: "y",
            value: ["cbo_diversity_eff", "cbo_diversity", "opp_gain"]
          });
        } else if (build.data_type === "secex") {
          defaults.ui.push({
            label: dataviva.dict.y,
            method: "y",
            value: ["pci", "opp_gain"]
          });
        }
      }
      if (build.app_type === "compare") {
        defaults.ui.push({
          label: dataviva.dict.scale,
          method: function(value, viz) {
            return viz.x({
              "scale": value
            }).y({
              "scale": value
            }).draw();
          },
          value: ["log", "linear"]
        });
        if (build.data_type === "rais") {
          defaults.ui.push({
            label: dataviva.dict.axes,
            method: function(value, viz) {
              return viz.x(value).y(value).draw();
            },
            value: ["num_emp", "wage", "wage_avg", "num_est"]
          });
        }
      }
      if (build.app_type === "network" || build.app_type === "rings" || build.app_type === "scatter") {
        defaults.ui.push({
          label: dataviva.dict.spotlight,
          method: function(value, viz) {
            value = value ? true : false;
            return viz.active({
              "spotlight": value
            }).draw();
          },
          value: [
            {
              "on": 1
            }, {
              "off": 0
            }
          ]
        });
        defaults.ui.push({
          label: dataviva.dict.rca_scope,
          method: function(value, viz) {
            return viz.active(function(d) {
              return d[value] >= 1;
            }).draw();
          },
          value: ["bra_rca", "wld_rca"]
        });
      }
      if (build.app_type === "stacked") {
        defaults.ui.push({
          label: dataviva.dict.sort,
          method: function(value, viz) {
            return viz.order({
              "sort": value
            }).draw();
          },
          value: ["asc", "desc"]
        });
        defaults.ui.push({
          label: dataviva.dict.layout,
          method: function(value, viz) {
            return viz.y({
              "scale": value
            }).draw();
          },
          value: ["linear", "share"]
        });
      }
      if (build.app_type === "occugrid") {
        defaults.ui.push({
          label: dataviva.dict.grouping,
          method: function(value, viz) {
            var grouping;
            grouping = value === "category";
            return viz.id({
              "grouping": grouping
            }).draw();
          },
          value: ["id", "category"]
        });
      }
      if (build.app_type === "stacked" || build.app_type === "occugrid") {
        defaults.ui.push({
          label: dataviva.dict.order,
          method: function(value, viz) {
            if (value === "name") {
              value = viz.text();
            }
            if (value === "value") {
              value = viz.size();
            }
            if (value === "color") {
              value = viz.color();
            }
            return viz.order(value).draw();
          },
          value: ["name", "value", "color"]
        });
      }
    }
    if (build.app_type === "line" || build.app_type === "bar") {
      defaults.ui.push({
        label: dataviva.dict.y_scale,
        method: function(value, viz) {
          return viz.y({
            "scale": value
          }).draw();
        },
        value: ["linear", "log"]
      });
    }
    if (build.demo && build.app_type === "bar" && build.data_type === "rais") {
      defaults.ui.push({
        label: dataviva.dict.y,
        method: "y",
        value: ["wage_avg", "num_emp"]
      });
    }
    params = configMerge(defaults, params);
    if (build.config.order) {
      if (build.demo && build.data_type === "sc" && build.app_type === "bar") {
        build.config.order = "course_sc_5";
      } else {
        build.config.order = true;
      }
    }
    params = configMerge(params, build.config);
    build.configured = true;
    return params;
  };

  window.visualization = function(builds) {
    var args, attr_type, build, div, filters, joiner, params, title, titleWidth, ui, uiWidth, _i, _len;
    if (!(builds instanceof Array)) {
      builds = [builds];
    }
    args = {};
    for (_i = 0, _len = builds.length; _i < _len; _i++) {
      build = builds[_i];
      build.container = build.container || d3.select("body");
      if (!d3plus.util.d3selection(build.container)) {
        build.container = d3.select(build.container);
      }
      div = build.container;
      build.id = div.attr("id") || div.attr("class") || div.node().localName;
      if (div.style("position") === "static") {
        div.style("position", "relative");
      }
      ui = div.append("div").attr("class", "visualization_ui");
      if (page !== "build") {
        ui.append("a").attr("alt", "comments").attr("href", build.url).append("i").attr("class", "fa fa-comments");
      }
      if (page !== "embed") {
        if (div.classed("lightbox")) {
          ui.append("a").attr("alt", "minimize").on(d3plus.client.pointer.click, function(d) {
            d3plus.tooltip.remove("alt_tooltip");
            return dataviva.lightbox();
          }).append("i").attr("class", "fa fa-compress");
        } else {
          ui.append("a").attr("alt", "enlarge").data([build]).on(d3plus.client.pointer.click, function(d) {
            d3plus.tooltip.remove("alt_tooltip");
            return dataviva.lightbox(function(elem) {
              var copy;
              copy = d3plus.util.copy(d);
              copy.container = elem;
              return visualization(copy);
            });
          }).append("i").attr("class", "fa fa-expand");
        }
      }
      uiWidth = ui.node().getBoundingClientRect().width;
      titleWidth = div.node().getBoundingClientRect().width - uiWidth * 2;
      titleWidth -= 200;
      title = page !== "build" ? build.title : false;
      dataviva.tooltip(ui.selectAll("a"));
      visualizations[build.id] = d3plus.viz().container(div.append("div").attr("class", "visualization_d3plus")).config(defaultStyle).error(dataviva.dict.loading + "...").margin(div.classed("lightbox") ? 10 : 0).title({
        height: ui.node().getBoundingClientRect().height,
        width: titleWidth,
        value: title
      }).draw();
      attr_type = build.display_attr;
      build.attr_url = "/attrs/" + attr_type + "/?lang=" + dataviva.language;
      build.data_url = "/" + build.url.split("/").slice(3).join("/");
      for (attr_type in build.filter_ids) {
        if (!(attr_type in trackedAttrs)) {
          trackedAttrs[attr_type] = [];
        }
        filters = build.filter_ids[attr_type].filter(function(f) {
          return trackedAttrs[attr_type].indexOf(f) < 0;
        });
        if (filters.length) {
          if (!(attr_type in args)) {
            args[attr_type] = [];
          }
          args[attr_type] = args[attr_type].concat(filters);
          trackedAttrs[attr_type] = trackedAttrs[attr_type].concat(filters);
        }
      }
    }
    params = "";
    joiner = "?";
    for (attr_type in args) {
      params += joiner + attr_type + "=" + d3.set(args[attr_type]).values().join(",");
      joiner = "&";
    }
    if (params.length && (builds.length > 1 || !builds[0].container.classed("lightbox"))) {
      setTimeout((function() {
        d3.json("/account/attr_view" + params).get();
      }), 5000);
    }
    return finish(builds);
  };

  urlChecks = ["attr_url", "coords", "network", "data_url"];

  finish = function(builds) {
    var nextURLs, readyBuilds;
    readyBuilds = [];
    nextURLs = builds.reduce(function(obj, build) {
      var extraData, url, _i, _len;
      if (build.demo && (!(demoURL in dataCache))) {
        if (!obj[demoURL]) {
          obj[demoURL] = [];
        }
        obj[demoURL].push(build);
        return obj;
      }
      for (_i = 0, _len = urlChecks.length; _i < _len; _i++) {
        url = urlChecks[_i];
        if (build[url] && (!(build[url] in dataCache))) {
          if (!obj[build[url]]) {
            obj[build[url]] = [];
          }
          obj[build[url]].push(build);
          return obj;
        }
      }
      if (!build.configured) {
        build.config = config(build);
      }
      extraData = build.config.extraData;
      if (extraData) {
        if (!(extraData in dataCache)) {
          if (!obj[extraData]) {
            obj[extraData] = [];
          }
          obj[extraData].push(build);
          return obj;
        }
        if (!(build.url in dataCache)) {
          dataCache[build.url] = build.config.dataMerge(build.config.data, dataCache[extraData]);
        }
        build.config.data = dataCache[build.url];
        delete build.config.dataMerge;
        delete build.config.extraData;
      }
      readyBuilds.push(build);
      return obj;
    }, {});
    checkData(nextURLs);
    return draw(readyBuilds);
  };

  checkData = function(urls) {
    var attr, attrURL, builds, data, stored, url, _results;
    _results = [];
    for (url in urls) {
      builds = urls[url];
      attrURL = url.indexOf("/attrs/") === 0;
      attr = url.indexOf("/attrs/d/") < 0 ? builds[0].display_attr : "d";
      stored = attrURL && Modernizr.localstorage && url in localStorage && ((!(attr in dataviva.storage)) || (parseFloat(localStorage[attr]) === dataviva.storage[attr]));
      if (dataCache[url]) {
        _results.push(finish(builds));
      } else if (stored) {
        data = JSON.parse(localStorage[url]);
        dataviva.depths[attr] = data.depths;
        dataCache[url] = dataviva.cleanData(data, attr, builds[0].display_key, attrURL, url);
        _results.push(finish(builds));
      } else {
        _results.push(loadData(url, builds));
      }
    }
    return _results;
  };

  loadData = function(url, builds) {
    var attr, attrURL, attr_key, coordURL, networkURL;
    attrURL = url.indexOf("/attrs/") === 0;
    coordURL = url.indexOf("/coords/") > 0;
    networkURL = url.indexOf("/networks/") > 0;
    attr = url.indexOf("/attrs/d/") < 0 ? builds[0].display_attr : "d";
    attr_key = builds[0].display_key;
    return d3.json(url, function(error, data) {
      if (!coordURL && !networkURL) {
        if (attrURL) {
          dataviva.depths[attr] = data.depths;
        }
        dataCache[url] = dataviva.cleanData(data, attr, attr_key, attrURL, url);
      } else {
        dataCache[url] = data;
      }
      if (attrURL && Modernizr.localstorage) {
        if (attr in dataviva.storage) {
          localStorage[attr] = dataviva.storage[attr];
          localStorage[url] = JSON.stringify(data);
        }
      }
      return finish(builds);
    });
  };

  draw = function(builds) {
    var build, viz, _i, _len, _results;
    _results = [];
    for (_i = 0, _len = builds.length; _i < _len; _i++) {
      build = builds[_i];
      console.log("D3plus configuration for \"" + build.title + "\":");
      console.log(build.config);
      _results.push(viz = visualizations[build.id].error(false).config(build.config).depth(build.config.depth).draw());
    }
    return _results;
  };

}).call(this);
