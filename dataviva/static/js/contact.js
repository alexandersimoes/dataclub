(function(){

  var listFormat = function(feed, activity){

    var formatDate = d3.time.format("%B %-d, %Y"),
        parseDate = d3.time.format.iso.parse;

    var questions = d3.select(feed).selectAll(".question_block")
      .data(activity, function(d){ return d.id; });

    var question_block = questions.enter()
      .insert("div", "div.infinite_loading")
        .attr("class", "accordion");

    var question_title = question_block.append("a")
      .attr("class", "decision")
      .text(function(d){ return d.question; })
      .on(d3plus.client.pointer.click,function(){
        var classed = d3.select(this.parentNode).classed("active");
        d3.select(this.parentNode).classed("active",!classed);
        classed = d3.select(this).classed("active");
        d3.select(this).classed("active",!classed);
      });

    // lastly, the div that holds the data
    var question_info = question_block.append("div")
      .attr("class","hidden");

    question_info.append("blockquote")
      .html(function(d){
        if (d.body) return d.body.replace(/<\/?[^>]+(>|$)/g, "");
        else d3.select(this).remove();
      });

    question_info.append("p")
      .html(function(d){
        return d.status_notes.replace(/<\/?[^>]+(>|$)/g, "");
      });

  };

  var order = null,
      search_term = null,
      json_url = "/ask/questions/?lang="+dataviva.language,
      is = infinite_scroll().format_items(listFormat);

  var change_order = function(new_order){
    order = new_order || orderForm.focus();
    var url = json_url + "&order=" + order;
    if(search_term){
      url += "&q=" + search_term;
    }
    d3.select("#question_feed").html('')
      .call(is.url(url).offset(0).remove(true));
  };

  var orderForm = d3plus.form()
    .data("[name=order]")
    .focus(undefined, change_order)
    .ui({"color": {"secondary": "#aaaaaa"}})
    .draw();

  change_order();

  d3.select("#ask_search").on("input", function(e){

    search_term = this.value;

    var url = json_url + "&q=" + search_term + "&order=" + order;

    d3.select("#question_feed").html('')
      .call(is.url(url).offset(0).remove(true));

  });

})();
