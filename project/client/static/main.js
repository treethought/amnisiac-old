// custom javascript

$( document ).ready(function() {
  console.log('Sanity Check!');

  // See what kind of device we're using
    var userAgent = navigator.userAgent.toLowerCase();
    var isAndroid = userAgent.indexOf('android') > -1;
    var isIpad = userAgent.indexOf('ipad') > -1;
    var isIphone = userAgent.indexOf('iphone') > -1;
console.log('User Agent is:')
console.log(navigator.userAgent.toLowerCase());

console.log(userAgent, isAndroid, isIphone);
});


