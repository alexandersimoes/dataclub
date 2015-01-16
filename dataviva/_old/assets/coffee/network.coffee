d3.json '/lattes/2013/all/show/all/?id', (error, json) ->
  nodeid2size = {}
  nodeid2size[row[0]] = row[1] for row in json.data
  d3.json '/static/json/lattes_network.json', (error, json) ->
    # normalize ids for nodes
    node.id = node.id.replace /,/g, '.' for node in json.nodes
    for edge in json.edges
      edge.source = edge.source.replace /,/g, '.'
      edge.target = edge.target.replace /,/g, '.'
    # end normalize

    d3color = d3.scale.category10()
    id2node = {}
    for node in json.nodes
      id2node[node.id] = node 
      if node.id not of nodeid2size
        console.log node.id
      else node.size = nodeid2size[node.id]
      node.color = node.id.split('.')[0]# + "." + node.id.split('.')[1]

    mean = d3.mean json.edges, (edge) -> edge.jaccard
    stdev = Math.sqrt d3.mean json.edges.map (edge) -> (edge.jaccard - mean)*(edge.jaccard - mean)
    json.edges.forEach (edge) -> edge.jaccard = (edge.jaccard - mean)/stdev
    
    json.edges = json.edges.filter (edge) -> edge.jaccard >= 2
    console.log '# of edges', json.edges.length
    #scale = d3.scale.linear()
    #  .domain d3.extent json.edges, (edge) -> edge.jaccard
    #  .range([0,10])
    d3edges = json.edges.map (edge) -> {source: id2node[edge.source], target: id2node[edge.target], jaccard:edge.jaccard}
    
    force = d3.layout.force()
    force
      .nodes(json.nodes)
      .links(d3edges)
      #.linkStrength (edge) -> edge.jaccard
     .start()
    force.tick() for i in [0...500]
    
    #document.write "<pre>"
    #for node in json.nodes
    #  document.write node.id + '\t' + node.x.toFixed(3) + '\t'+ node.y.toFixed(3) + '\n'
    #document.write "</pre>"
    

    visualization = d3plus.viz()
      .container("#viz")
      .type("network")
      .data(json.nodes)
      .nodes(json.nodes)
      .nodes {overlap: 1.5}
      .edges(json.edges)
      .id("id")
      .size "size"
      .size {scale: d3.scale.linear()}
      #.id(["parentID","id"])
      #.depth(1)
      #.text({parentID: "parentEnName", id:"enName"})
      .text("enName")
      .color "color"
      # .color (node) -> node.color
      #.color("parentID")
      .draw()