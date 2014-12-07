$(function () {

    Highcharts.setOptions({
        global : {
            useUTC : false
        }
    });

    // Create the chart
    $('#graph').highcharts('StockChart', {
        chart : {
            events : {
                load : function () {

                    // set up the updating of the chart each second
                    var series = this.series[0];
		    $(document).on("sentiment", function(x,y){
                        var x = (new Date()).getTime(); // current time
			series.addPoint([x,y], true, false);
		    });
/*
                    setInterval(function () {
                        var x = (new Date()).getTime(), // current time
                            y = Math.round(Math.random() * 200 - 100);
                        series.addPoint([x, y], true, false);
			console.log(y);
                    }, 1000);
*/
                }
            }
        },

        rangeSelector: {
            buttons: [{
                count: 1,
                type: 'minute',
                text: '1M'
            }, {
                count: 5,
                type: 'minute',
                text: '5M'
            }, {
                type: 'all',
                text: 'All'
            }],
	    allButtonsEnabled: true,
            inputEnabled: false,
            selected: 2
        },

        title : {
            text : 'Realtime tweet sentiment data'
        },

        exporting: {
            enabled: false
        },

        series : [{
            name : 'Tweet sentiment data',
            data : (function () {
                // generate an array of random data
                var data = [], time = (new Date()).getTime(), i;
		
                for (i = 1; i <= 0; i += 1) {
                    data.push([
                        time + i * 1000,
                        Math.round(Math.random() * 100) * 0
                    ]);
                }
                return data;
            }())
        }]
    });

});

var SAMPLE_SIZE = 10;

var tweets = [];
var oldest_tweet = (new Date()).getTime();
$(document).on("msg", function(tweet) {
    //add tweets to process
    tweets.push(tweet);
    //update oldest date if this one is older than previous one
    if(tweet.date < oldest_tweet.date) {
	oldest_tweet = tweet;
    }
    //add average sentiment graph if we achieved minimum sample points required
    if(tweets.length > SAMPLE_SIZE) {
	var sum = 0;
	while(tweets.lenght > 0) {
	    sum = sum + tweets.pop().val;
	}
    	$(document).trigger("sentiment", [(new Date()).getTime()]);
    }
});
