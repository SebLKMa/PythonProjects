https://jsfiddle.net/
HTML:
<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>
<ul id="parent"></ul>
JAVASCRIPT:
var tree = [{
  text: "Parent 1",
  nodes: [{
    text: "Child 1",
    nodes: [{
      text: "Grandchild 1",
      nodes: [{
        text: "GrandChild 3"
      }]
    }, {
      text: "Grandchild 2",
      nodes: [{
        text: "GrandChild 4"
      }]
    }]
  }, {
    text: "Child 2"
  }]
}, {
  text: "Parent 2"
}, {
  text: "Parent 3"
}, {
  text: "Parent 4"
}, {
  text: "Parent 5"
}];

function recursive_tree(data, tag, child_wrapper, level) {
  var html = [];
  //return html array;
  level = level || 0;
  child_wrapper = (child_wrapper != false) ? child_wrapper : 'ul';
  $.each(data, function(i, obj) {
    var el = $('<' + tag + '>');
    el.html(obj.text);
    if (obj.hasOwnProperty('nodes')) {
      var wrapper = $('<' + child_wrapper + '>');
      var els = recursive_tree(obj.nodes, tag, child_wrapper);
      wrapper.append(els);
      wrapper.appendTo(el);
    }
    html.push(el);
  });
  return html;
}

$(document).ready(function() {
  var html = recursive_tree(tree, 'li', 'ul');
  console.log(html);
  $('#parent').append(html);

});



{
"id": "example:Package-032c2f17-fa25-4dcb-898a-0381cd82625f", 
"version": "1.2", 
"observables": {"major_version": 2, "minor_version": 1, "update_version": 0}, 
"incidents": 
[
{"id": "example:incident-b26c5658-e229-43a6-a579-d5c4b73aa043", 
"title": "The Multi-sig Hack", 
"description": "Parity Wallet Hacked", 
"timestamp": "2017-11-30T07:00:33.348043+00:00", 
"related_indicators": {}, 
"related_observables": {}, 
"related_incidents": {}, 
"related_packages": {}, 
"leveraged_ttps": {}, 
"confidence": {
  "timestamp": "2017-11-30T07:00:33.348043+00:00", "timestamp_precision": "second", "value": "High"
}, 
"reporter": {
  "identity": {"name": "parity technologies ltd"}, 
  "description": "https://paritytech.io/blog/security-alert.html", 
  "time": {"produced_time": "2017-11-08T00:00:00"}
}, 
"time": {
  "initial_compromise": "2017-11-06T00:00:00", 
  "incident_discovery": "2017-11-08T00:00:00", 
  "incident_reported": "2017-11-08T00:00:00"
}, 
"impact_assessment": {
  "effects": ["Estimated Loss of $280m in Ether"]
}, 
"victims": [{"name": "Cappasity"}, {"name": "Who else ?"}]
}
], 
"ttps": {"kill_chains": {}}
}

POINTS
======
https://paritytech.io/blog/security-is-a-process-a-postmortem-on-the-parity-multi-sig-library-self-destruct.html
STIX Object Model
STIX stable version 1.2 vs 2.0 - stable tools and documentation ?
STIX Incident structure - can this be used standalone ?

STIX is a information sharing () data Model
You underlyimg database is independent of it.



