/*****************************************/
// Name: Javascript Textarea HTML Editor
// Version: 1.3
// Author: Balakrishnan
// Last Modified Date: 25/Jan/2009
// License: Free
// URL: http://www.corpocrat.com
/******************************************/

var textarea;
var content;

function doImage(obj){
	textarea = document.getElementById(obj);
	var url = prompt('Enter the Image URL:','http://');

	var scrollTop = textarea.scrollTop;
	var scrollLeft = textarea.scrollLeft;

	if (url != '' && url != null) {
		if (document.selection) {
			textarea.focus();
			var sel = document.selection.createRange();
			sel.text = '<img src="' + url + '">';
		} else {
			var len = textarea.value.length;
		    var start = textarea.selectionStart;
			var end = textarea.selectionEnd;

	        var sel = textarea.value.substring(start, end);
		    //alert(sel);
			var rep = '<img src="' + url + '">';
	        textarea.value =  textarea.value.substring(0, start) + rep + textarea.value.substring(end, len);
			textarea.scrollTop = scrollTop;
			textarea.scrollLeft = scrollLeft;
		}
	}
}

function doURL(obj){
	var sel;
	textarea = document.getElementById(obj);
	var url = prompt('Enter the URL:','http://');
	var scrollTop = textarea.scrollTop;
	var scrollLeft = textarea.scrollLeft;

	if (url != '' && url != null) {
		if (document.selection){
			textarea.focus();
			var sel = document.selection.createRange();

			if(sel.text==""){
				sel.text = '<a href="' + url + '">' + url + '</a>';
				} else {
				sel.text = '<a href="' + url + '">' + sel.text + '</a>';
				}
			//alert(sel.text);
		} else {
			var len = textarea.value.length;
		    var start = textarea.selectionStart;
			var end = textarea.selectionEnd;

			var sel = textarea.value.substring(start, end);

			if(sel==""){
				sel=url;
			} else {
	        	var sel = textarea.value.substring(start, end);
			}
		    //alert(sel);

			var rep = '<a href="' + url + '">' + sel + '</a>';;
	        textarea.value =  textarea.value.substring(0,start) + rep + textarea.value.substring(end,len);
			textarea.scrollTop = scrollTop;
			textarea.scrollLeft = scrollLeft;
		}
	}
}

function doAddTags(tag1, tag2, obj){
    textarea = document.getElementById(obj);

	// Code for IE
	if (document.selection){
		textarea.focus();
		var sel = document.selection.createRange();
		var index_of_two = sel.indexOf('<','>');
		var index_of_slash = sel.indexOf('</','>');
		// alert(sel.text);
		if (sel) {
			if (index_of_two >= '0' && index_of_slash >= '0' || index_of_two == '-1' && index_of_slash == '-1') {
				sel.text = tag1 + sel.text + tag2;
			}
		}
	} else {  // Code for Mozilla Firefox
		var len = textarea.value.length;
	    var start = textarea.selectionStart;
		var end = textarea.selectionEnd;

		var scrollTop = textarea.scrollTop;
		var scrollLeft = textarea.scrollLeft;

        var sel = textarea.value.substring(start, end);
		var index_of_two = sel.indexOf('<','>');
		var index_of_slash = sel.indexOf('</','>');
	    // alert(sel);
		// alert('index_of_two = '+index_of_two);
		// alert('index_of_slash = '+index_of_slash);
		if (sel) {
			if (index_of_two >= '0' && index_of_slash >= '0' || index_of_two == '-1' && index_of_slash == '-1') {
				var rep = tag1 + sel + tag2;
		        textarea.value =  textarea.value.substring(0, start) + rep + textarea.value.substring(end, len);

				textarea.scrollTop = scrollTop;
				textarea.scrollLeft = scrollLeft;
			}
		}
	}
}

function doList(tag1, tag2, obj){
	textarea = document.getElementById(obj);

	// Code for IE
	if (document.selection){
		textarea.focus();
		var sel = document.selection.createRange();
		var list = sel.text.split('\n');

		for(i=0;i<list.length;i++)
		{
		list[i] = '<li>' + list[i] + '</li>';
		}
		//alert(list.join("\n"));
		sel.text = tag1 + '\n' + list.join("\n") + '\n' + tag2;
	} else {
		// Code for Firefox
		var len = textarea.value.length;
	    var start = textarea.selectionStart;
		var end = textarea.selectionEnd;
		var i;

		var scrollTop = textarea.scrollTop;
		var scrollLeft = textarea.scrollLeft;

	    var sel = textarea.value.substring(start, end);
		var index_of_two = sel.indexOf('<','>');
		var index_of_slash = sel.indexOf('</','>');
	    // alert(sel);

		if (sel) {
			if (index_of_two >= '0' && index_of_slash >= '0' || index_of_two == '-1' && index_of_slash == '-1') {
				var list = sel.split('\n');

				for(i=0; i<list.length; i++){
					list[i] = '<li>' + list[i] + '</li>';
				}
				// alert(list.join("<br>"));

				var rep = '\n' + tag1 + '\n' + list.join("\n") + '\n' + tag2 + '\n';
				textarea.value =  textarea.value.substring(0, start) + rep + textarea.value.substring(end, len);

				alert('rep = '+rep);
				alert('textarea = '+textarea.value);

				textarea.scrollTop = scrollTop;
				textarea.scrollLeft = scrollLeft;
			}
		}
	}
}
