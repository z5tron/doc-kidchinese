
// function showNextWord() {
//     console.log( "ready!" );
//     $.ajax({
//         type: 'GET',
//         url: "next",
//         dataType: 'json',
//         success: function(data) {
//             console.log("Next:", data); $(':input[name="wordId"]').val(data["wordId"]);
//             $('#word').text(data["word"]);
//             $('span#wordId').text(data["wordId"]);
//             $('p#dateModified').text(data["dateModified"]);
//             $('p#wordStat').text(data["wordId"] + ": " + data["countPass"] + "/" + data["countFail"]);
//         }
//     });
// }

// $( document ).ready(function() {
//     console.log( "ready!" );
//     // showNextWord();
// });


// $('#btn-skip').click(function() {
//     $.ajax({
//         type: 'GET',
//         url: "skip",
//         data: {wordId: $("input[name=wordId").val()},
//         dataType: 'json',
//         success: function(data) { console.log(data); showNextWord(); }
//     });
//     console.log("passed ?");
// })

// $('#btn-pass').click(function() {
//     $.ajax({
//         type: 'GET',
//         url: "pass",
//         data: {wordId: $("input[name=wordId").val()},
//         dataType: 'json',
//         success: function(data) { console.log(data); showNextWord(); }
//     });
//     console.log("passed ?");
// })

// $('#btn-fail').click(function() {
//     $.ajax({
//         type: 'GET',
//         url: "fail",
//         data: {wordId: $("input[name=wordId").val()},
//         dataType: 'json',
//         success: function(data) { console.log(data); showNextWord(); }
//     });
//     console.log("passed ?");
// })

// $('#btn-add').click(function() {
//     $.ajax({
//         type: 'GET',
//         url: "add",
//         data: {w: $("input[name=addword1").val()},
//         dataType: 'json',
//         success: function(data) { console.log(data); $("input[name=addword1]").val(""); }
//     });
//     console.log("passed ?");
// })

var app = new Vue({
  el: '#wordapp',
  data: {
    words: [],
    totalWords: 0,
    message: 'Hello Vue!'
  },
  computed: {
  },
  methods: {
    markPoints: function(word, score) {
      var dt = new Date();
      console.log("marking ", word.word, "right");
      console.log(dt.toISOString());
      this.$set(word, 'score', score);
      this.$set(word, 'dateStudy', dt.toISOString());
      this.saveWords([ word ]);
    },
    skipWord: function(word) { word.skip = true; },
    status: function(word) {
      if (word.score == 0) return 'new';
      else if (word.score < 0) return 'wrong';
      else return 'pass';
    },
    show: function(word) {
      if (word.skip) return false;
      if (word.score > 0) return false;
      return true;
    },
    saveWords: function(words) {
      var self = this;
      console.log(JSON.stringify(words));
      $.ajax({
	type: 'POST',
	url: './save',
	contentType:"application/json",
	data: JSON.stringify(words),
	dataType: 'json',
	success: function(data) {
	  console.log("saved!");
	},
	error: function(data) { alert("ERROR"); },
      });
    }
  },
  mounted: function() {
    var self = this;
    $.ajax({
      type: 'GET',
      url: "words",
      dataType: 'json',
      success: function(data) {
	console.log(data);
	self.words.splice(0);
	self.totalWords = data.totalWords;
	for (var i = 0; i < data.words.length; ++i) {
	  data.words[i].score = 0;
	  data.words[i].skip = false;
	  // data.words[i].dateStudy = '';
	  self.words.push(data.words[i]);
	}
      }
    });
    console.log("passed ?");
  },
})
