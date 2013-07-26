$(document).ready(function(){
  $('#search').on('click', search);
})


function search(){
  var topic = $('input').val();

  var json = $.ajax({ url: 'http://192.168.1.48:8983/solr/select/?q=text:%22' + topic + '%22&sort=retweet_count%20desc&wt=json&facet=on&facet.field=user_name&facet.field=ner_location', dataType: 'json', success: function(data){
    users = data.facet_counts.facet_fields.user_name
    locations = data.facet_counts.facet_fields.ner_location
    docs = data.response.docs

    $.each(users, function(i, v){
      $('<p>' + v + '</p>').appendTo('#users');
    });

    $.each(locations, function(i, v){
      $('<p>' + v + '</p>').appendTo('#locations');
    });

    $.each(docs, function(i, v){
      $('<p>' + v.user_name + '-'+ v.text +  '-' + v.retweet_count + '</p>').appendTo('#docs');
    });
 }})


}
