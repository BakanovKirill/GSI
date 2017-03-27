<html>

<head>
<meta charset="UTF-8" />
<title>GSi Maps</title>
<script type='text/javascript' src='js/jquery.js?ver=1.4.4'></script>

<!-- start google maps gpx plugin api loader -->
<script type="text/javascript" src="https://www.google.com/jsapi"></script>
<script type="text/javascript" id="script">google.load('visualization', '1', {packages: ['corechart']});</script>
<script type="text/javascript" src="js/gmap_v3_elevation.js"></script>
<script type="text/javascript">google.load("maps", "3", {other_params:"sensor=false&libraries=places,drawing,panoramio"});</script>
<script type="text/javascript" src="js/gmap_v3_size.js"></script>
<script type="text/javascript" src="js/gmap_v3_gpx_overlay.js"></script>
<script type="text/javascript" src="js/gmap_v3_wms_overlay.js"></script>
<script type="text/javascript" src="js/gmap_v3_init.js"></script>
<script type="text/javascript" src="js/gmap_v3_edit.js"></script>
<link rel="stylesheet" href="js/gmap_v3.css" type="text/css" />
<!-- end google maps gpx plugin api loader -->

	<script type="text/javascript" src="ExtDraggableObject.js"></script>
	<script type="text/javascript" src="CustomTileOverlay.js"></script>
	<script type="text/javascript">
		/*******************************************************************************
		Copyright (c) 2010-2012. Gavin Harriss
		Site: http://www.gavinharriss.com/
		Originally developed for: http://www.topomap.co.nz/

		Licences: Creative Commons Attribution 3.0 New Zealand License
		http://creativecommons.org/licenses/by/3.0/nz/
		******************************************************************************/

		var OPACITY_MAX_PIXELS = 57; // Width of opacity control image
		var map, overlay;
		
		function init_slider() {
			// Map options for example map
			var mapOptions = {
				zoom: 13,
				minZoom: 13,
				maxZoom: 13,
				center: new google.maps.LatLng(-42.8598, 171.8043),
				disableDefaultUI: true,
				mapTypeId: google.maps.MapTypeId.SATELLITE,
				navigationControl: false,
				mapTypeControl: false,
				scaleControl: false,
				zoomControl: false,
				panControl: false
			}
			//map = new google.maps.Map(document.getElementById("map_1"), mapOptions);
			map = map_1;

			var initialOpacity = 75;

			overlay = new CustomTileOverlay(map, initialOpacity);
			overlay.show();

			google.maps.event.addListener(map, 'tilesloaded', function () {
				overlay.deleteHiddenTiles(map.getZoom());
			});

			// Add opacity control and set initial value
			createOpacityControl(map, initialOpacity);
		}

		function createOpacityControl(map, opacity) {
			var sliderImageUrl = "opacity-slider2.png";
			
			// Create main div to hold the control.
			var opacityDiv = document.createElement('DIV');
			opacityDiv.setAttribute("style", "margin:5px;overflow-x:hidden;overflow-y:hidden;background:url(" + sliderImageUrl + ") no-repeat;width:71px;height:21px;cursor:pointer;");

			// Create knob
			var opacityKnobDiv = document.createElement('DIV');
			opacityKnobDiv.setAttribute("style", "padding:0;margin:0;overflow-x:hidden;overflow-y:hidden;background:url(" + sliderImageUrl + ") no-repeat -71px 0;width:14px;height:21px;");
			opacityDiv.appendChild(opacityKnobDiv);

			var opacityCtrlKnob = new ExtDraggableObject(opacityKnobDiv, {
				restrictY: true,
				container: opacityDiv
			});

			google.maps.event.addListener(opacityCtrlKnob, "dragend", function () {
				var value = (100 / OPACITY_MAX_PIXELS) * opacityCtrlKnob.valueX()	
				setOpacity(value);
			});

			google.maps.event.addDomListener(opacityDiv, "click", function (e) {
				var left = findPosLeft(this);
				var x = e.pageX - left - 5; // - 5 as we're using a margin of 5px on the div
				opacityCtrlKnob.setValueX(x);
				var value = (100 / OPACITY_MAX_PIXELS) * x;
				setOpacity(value);
			});

			map.controls[google.maps.ControlPosition.BOTTOM_CENTER].push(opacityDiv);
			//map_1.controls[google.maps.ControlPosition.BOTTOM_CENTER].push(opacityDiv);

			// Set initial value
			var initialValue = OPACITY_MAX_PIXELS / (100 / opacity);
			opacityCtrlKnob.setValueX(initialValue);
			var value = (100 / OPACITY_MAX_PIXELS) * initialValue;
			setOpacity(value);
		}

		function setNewOpacity(pixelX) {
			// Range = 0 to OPACITY_MAX_PIXELS
			var value = (100 / OPACITY_MAX_PIXELS) * pixelX;
			if (value < 0) value = 0;
			if (value == 0) {
				if (overlay.visible == true) {
					overlay.hide();
				}
			}
			else {
				overlay.setOpacity(value);
				if (overlay.visible == false) {
					overlay.show();
				}
			}
		}

		function findPosLeft(obj) {
			var curleft = 0;
			if (obj.offsetParent) {
				do {
					curleft += obj.offsetLeft;
				} while (obj = obj.offsetParent);
				return curleft;
			}
			return undefined;
		}
		
var selRegion = "Region";
var newSelRegion = "";
var opts = [];
var prevopts = [];
var KMLopts = [];
var count = 0;
var called_redraw = 0;
var new_region = 1;
var optlist = "";

var AllowDrawing=0;  // set to 1 to enable creation and saving of polygons

<?php

$specfile = $_REQUEST["q"];
$DisplayMode = $_REQUEST["x"];

$phpPath=__FILE__ ;
$RootPart=substr($phpPath,19,strlen($phpPath)-19-4);

echo 'console.log("FILE= '. $phpPath.', RootPart='.$RootPart.'");' . "\n";

if ( (strlen($RootPart)<=2) || (strpos($RootPart,"Poly")>0))
{
   $RootPath=".";
   $AllowPolygonDisplay=1; // set to 1 to allow display and overlay of polygons
   echo "AllowDrawing=1; \n";
}
else
{
//   $RootPath="FiniteNY";
   $RootPath=$RootPart;
   if (!isset($_REQUEST["q"]))
   {
//   	   $specfile = "images/*." . $RootPart;
   	   $specfile = "images/*";
   }
   $AllowPolygonDisplay=0; // set to 1 to allow display and overlay of polygons
   echo "AllowDrawing=0; \n";
}

$ind=0;
$kmlopts = array();
$numkmlopts=0;
foreach (glob($RootPath."/kml/*.kml") as $input) {
   preg_match('~kml/(.*?).kml~', $input, $output);
   echo 'KMLopts['.$ind.'] = "'.$output[1].'";'."\n";
   $kmlopts[$ind] = $output[1];
   $ind = $ind+1;
}
$numkmlopts=$ind;
?>

function fetch_select(val,mode,count)
{
   //opts = [];
   var request;
   var response = "";
   var images = val.split(',');

   var xmlhttp = new XMLHttpRequest();	
   if ((mode==1)|| (mode==3))
   {
   	  if (val!=selRegion)
   	  {
   	  	  new_region=1;
   	  	  newSelRegion = val;
      }
      selRegion = val;
      request = val;
      document.getElementById("selRegion").innerHTML = selRegion;
   }
   else if (mode==2)
   {
   	   request = images[0] + "." + selRegion;
   }
   
   xmlhttp.onreadystatechange = function ()
   {
      if (xmlhttp.readyState == 4 && xmlhttp.status == 200)
      {
      	   response = xmlhttp.responseText;
      	   //console.log("response="+response);
      	   
      	   if (mode==1)
      	   {
       	      document.getElementById("checkmenu").innerHTML=response; 
     	      var list = response.match(/<li><a>(.*)input/g);
      	      newlist="";
      	      //window.alert("document.URL="+document.URL);
      	      for (ind=0;ind<list.length;ind++)
      	      {
      	         var newname = list[ind].substring(7,list[ind].length-6);
      	         newlist = newlist + newname + ":";
      	         opts[ind] = newname;
 //     	         if ((called_redraw==0) && (document.URL.includes(newname)))
      	         if (( called_redraw==0) )
      	         {
      	         	 //document.getElementById(newname).checked = true;
      	         	 optlist = optlist + newname + ",";
      	         }
      	         else if ( (called_redraw!=0) && (new_region==1) )
      	         {
       	         	 for (i=0;i<prevopts.length;i++)
      	         	 {
      	         	 	 if (newname == prevopts[i]) document.getElementById(newname).checked = true;
      	         	 }
      	         }
      	      }
      	      // Now need to update list of DEM overlay files, if any (for selected AoI)
      	      fetch_select(val,3,count);
      	   }
      	   else if (mode==2)
      	   {
      	   	   //window.alert("Response is:" +response);
      	   	   var lims = response.split(',');
      	   	   count = overlays.length;
      	   	   for (ind=0;ind<images.length-1;ind++)
      	   	   {
      	   	      var image = RootPath+"/png/" + images[ind] + "." + selRegion + ".png";
       	   	      //var image = val;
      	   	      addImage(image,lims[0],lims[1],lims[2],lims[3]);
      	   	      imagedata[count++] = images[ind];
                  document.getElementById('data').value = images[ind];
                  //console.log("Adding check for: "+images[ind]);
                  //if (document.getElementById(images[ind])!=null)
                  //   document.getElementById(images[ind]).checked = true;
      	   	   }
      	   	   //post_init(map_1); // want to resore to previous viewPort!
      	   }
      	   if (mode==3)
      	   {
      	   	   //console.log("DEM menu settings:"+response);
        	   document.getElementById("DEMmenu").innerHTML=response; 
     	   }
      	   else
      	   {
      	     prevopts = [];
      	     i=0;
     	     for (ind=0;ind<opts.length;ind++)
     	     {
     	   	   if ( document.getElementById(opts[ind])!=null)
     	   	   {
     	   	      if ( document.getElementById(opts[ind]).checked )
      	             prevopts[i++] = opts[ind];
      	       }
      	     }
      	   }

       }
   };
   xmlhttp.open("POST","GetMenuOpt.php",true);
   xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
   console.log("GetMenuOpt request: q="+request+"&r="+mode+"&s="+RootPath);
   xmlhttp.send("q="+request+"&r="+mode+"&s="+RootPath);  
}

function redraw()
{
   // Get selected region and (multichoice) attribute(s) and KML overlay(s)
   //window.alert("selRegion="+selRegion);
   called_redraw = 1;

   // only want to reset images if region has changed since last time!!
   //
   for (i in overlays) overlays[i].setMap(null);
   overlays = [];
   count = 0;
   //
   
   var allopts = "";
   optlist = "";
   if (opts.length>0)
   {
     for (ind=0;ind<opts.length;ind++)
     {
     	 if (document.getElementById(opts[ind])!=null)
     	 {
   	        allopts = allopts+opts[ind]+":"+document.getElementById(opts[ind]).checked+", ";
            if (document.getElementById(opts[ind]).checked)
            {
                 optlist = optlist+opts[ind]+",";
                 //var imgfile = opts[ind] + "." + selRegion;
            }
         }
     }
   }
   //window.alert("allopts="+allopts);
   if (optlist.length>0)
   {
        //window.alert("Add image overlays: "+optlist+", num overlays="+overlays.length);
        //set_cookie(map_1,true);
        fetch_select(optlist,2,0);            
   }
   //console.log("redraw: Using options: "+optlist);
 
   if (KMLopts.length>0)
   {
   	 for (ind=0;ind<kmloverlays.length;ind++)
   	   kmloverlays[ind].setMap(null);
   
     // need to reset kmloverlays...
   	 kmloverlays = [];
     for (ind=0;ind<KMLopts.length;ind++)
     {
/*
        if (newSelRegion != "")
     	{
     		if (KMLopts[ind] == "Harvest_"+newSelRegion )
     			document.getElementById(KMLopts[ind]).checked = true;
     		else
     		    document.getElementById(KMLopts[ind]).checked = false;
     	}
*/     
      if (document.getElementById(KMLopts[ind])!=null)
      {
        if (document.getElementById(KMLopts[ind]).checked)
        {
       	    // may need special case of GetMenuOpt to get root URL info?
       	    console.log("document.URL="+document.URL);
       	    endpos = document.URL.indexOf("GSiMap");
       	    
            //var kmlfile = "http://www.eo.ukmm.com/GSiMaps/kml/" + KMLopts[ind] + ".kml";
            var kmlfile ;
            if (RootPath==".")
               kmlfile =  document.URL.substring(0,endpos) + "kml/" + KMLopts[ind] + ".kml";
           else
               kmlfile =  document.URL.substring(0,endpos) + RootPath + "/kml/" + KMLopts[ind] + ".kml";
          
            console.log("Add KML overlay: "+kmlfile);
            addKMLoverlay(kmlfile);
        }
      }
     }
     newSelRegion="";
   }

}

</script>

<link rel="stylesheet" type="text/css" href="menu_style.css">

</head>

<body class="page page-id-1685 page-child parent-pageid-406 page-template page-template-default">

<script type="text/javascript" src="http://code.jquery.com/jquery-1.7.2.min.js"></script>
<script type="text/javascript" src="menu_script.js"></script>

<div id="header"></div>   
<div id="content"> <!-- Start of content -->
<div class="container">
<div class="entry-content">
 
<?php

// Restrict access to current directory and to linked dirs on lustre
$allowed_paths=getcwd().":/lustre/w23/Satellite/WebData/";
//$allowed_paths="/lustre/w23/Satellite/WebData/";
//ini_set('open_basedir', $allowed_paths);

//$fileWildName="images/HeightLidarObs_*OneScene";
$RootWildFileName=$RootPath."/images/HeightLidarObs_*OneScene";

// Determine operational mode (ie value for "x") from specified filename
// First, strip off "images/" if present (and add it, for pngrefile)
if (strpos($specfile, 'images') !== false) {
   $pngrefile = $RootPath."/".$specfile;
   $RootWildFileName = substr($specfile,7);
} else {
   $pngrefile = $RootPath.'/images/'.$specfile;
   $RootWildFileName = $specfile;
}

$DisplayMode = 2;

// Look for "*" within filename
$fileWildName=$RootPath."/images/".$RootWildFileName;
$StartWildPos = strpos($RootWildFileName, '*');
if (strpos($RootWildFileName, '*') !== false) {
   $DisplayMode = 4;
   $WildRemaining = substr($RootWildFileName,$StartWildPos+1);
//   $PossibleYear = substr($RootWildFileName,$StartWildPos-4,4);
//   if (($PossibleYear=="2015") || ($PossibleYear=="2016")) {
//      $StartWildPos = $StartWildPos - 4; // show year as well as wild-carded Month/Day	
//   }

//   $StartWildPos = $StartWildPos + 4; // to allow for later prefixing of ".png"
  
   foreach (glob($fileWildName.".tif") as $pngfile) {
      $pngrefile = substr($pngfile,0,strpos($pngfile, '.tif'));
   }
}

echo '<script type="text/javascript">'."\n";
echo "var presetpngfile = \"".str_replace("images","png",$pngrefile) . '.png'."\";\n";
echo "var RootPath = \"".$RootPath."\";\n";
echo "console.log('RootPath='+RootPath);\n";
echo '</script>'."\n";

if ($DisplayMode==null)
{
   echo 'Param: <input type="text" id="param" style="width: 250px;" placeholder="param">'."\n";
   echo 'MultiFile: <input type="text" id="multifile" style="width: 250px;" placeholder="multifile">'."\n";
   echo 'Display: <select id="chart"> <option value="0">Show Values</option><option value="1">Line Chart</option><option value="2">Bar Chart</option><option value="3">Pie Chart</option></select>'."\n";
   echo "<br>\n";
   $DisplayMode="0";
}
else
{
   echo '<input type="hidden" id="param" placeholder="param">'."\n";
   echo '<input type="hidden" id="multifile" placeholder="multifile">'."\n";
   echo '<input type="hidden" id="chart" placeholder="chart" value="0">'."\n";
   if ($DisplayMode=="4")
   {
        echo '<script type="text/javascript">'."\n";
   	echo 'document.getElementById("multifile").value = "'.$fileWildName.'"'."\n";  
   	echo 'document.getElementById("chart").value = "0"'."\n"; 
        echo '</script>'."\n";
   }
}
?>

<input type="hidden" id="showpix" placeholder="showpix">
<table><tr>
<!--
<td>Lat: <input type="text" id="latitude" style="width: 80px;" placeholder="latitude"> </td>
<td>Lon: <input type="text" id="longitude" style="width: 80px;" placeholder="longitude"> </td>
-->

<?php
/*
   if ($DisplayMode=="4")
   {
      echo '<td> Data: <input type="text" id="data" style="left: 600px; width: 100px;" placeholder="data"></td>';
      echo '<td><input type="button" value="Step Image Overlay" onclick="cycleImageOverlays();" /></td>';
   }
*/
?>
<td style="height:30px;">
<div class="container" id="menu">
<a class="toggleMenu" >Menu</a>
<ul class="nav">
	<li>
	  <a><div id="selRegion">Region</div></a>
		<ul>
		<?php
		// Get list of available AoIs...
		$names = array();
		$num = 0;
		foreach (glob($RootPath."/images/*.tif") as $input) {
		   $inprev=strrev($input);
		   preg_match('~fit.(.*?)[_\.]~', $inprev, $outrev);
		   $outfwd=strrev($outrev[1]);
		   //echo $input . " : " . $outfwd . "\n<br>";
		   $found = 0;
		   for ($i=0;$i<$num;$i++)
		   {
			  if ($outfwd==$names[$i]) $found=1;
		   }
		   if ($found==0) 
		   {
			  $names[$num] = $outfwd;
			  $num++;
			  //echo $outfwd . "\n<br>";
			  echo '<li><a onclick="fetch_select('. "'" .$outfwd. "'". ',1,0);" >' .$outfwd. "</a></li>";
		   }
		}
		
		// populate list of params for initial AoI, or AoI matching that in command line!
		$matchlen=0;
		$match = -1;
		for ($ind=0;$ind<$num;$ind++)
		{
			if (strpos($pngrefile,$names[$ind]) > 0)
			{
				if (strlen($names[$ind])>$matchlen)
				{
					$match = $ind;
					$matchlen = strlen($names[$ind]);
				}
			}
		}
		if ($match>=0)
		{
		   //echo "<script>window.alert('num=".$num.", match=".$match."');</script>";
		   echo "<script>fetch_select('".$names[$match]."',1,0);</script>";
		}
		?>
		</ul>
    </li>
	<li>
		<a >Attributes</a>
		<ul>
           <div id="checkmenu"></div>
        </ul>
    </li>
	<li>
		<a >3D Terrain</a>
		<ul>
           <div id="DEMmenu"></div>
        </ul>
    </li>
<?php
   if ($AllowPolygonDisplay==1)
   {
	   echo '<li>';
	   echo '	<a >Polygons</a>';
	   echo '		<ul>';
        foreach (glob($RootPath."/kml/*.kml") as $input) 
        {
           preg_match('~kml/(.*?).kml~', $input, $output);
           $checked = "";
           if (strpos($output[1],"Harvest_") !== false)
           {
           	  $kmlAoI = substr($output[1],8,strlen($output[1])-8);
           	  //echo "<script>window.alert('output=".$output[1].", kmlAoI=".$kmlAoI."');</script>";
              if (strpos($pngrefile,$kmlAoI) > 0) 
              { 
           	     $checked = "checked";
           	     //echo "<script>window.alert('attr=".$output[1].", checked=".$checked."');</script>";
              }
          }
           echo '<li><a>'.$output[1].'<input type="checkbox" id="'.$output[1].'" style="float:left;" ' . $checked . '/></a></li>';
        }
       echo '    </ul>';
       echo '</li>';
   }
?>    
	<li>
		<a onclick="redraw();" >Hide/Show</a>
		<ul>
		   <li><a onclick="toggleImageOverlays();"><input type="checkbox" id="ToggleImage" style="float:left;"/>Image Overlay</a></li>
		   <?php
		      if ($AllowPolygonDisplay==1)
		      {
		         echo '<li><a onclick="toggleKmlOverlays();"><input type="checkbox" id="ToggleImage" style="float:left;"/>Polygon Overlay</a></li>';
		      }
		   ?>
        </ul>
    </li>
	<li>
		<a onclick="redraw();" >Redraw</a>
		<ul>
        </ul>
    </li>
</ul>
</div>
</td></tr>
</table>

<div class="google_map_holder" id="map_1" style="width:auto;  height:600px;  border: 1px  solid black;"></div> 

<script type="text/javascript">


		var fszIndex = 1;
		var distanceUnit = "";
		
		var scrollToEle = "html";
		var mapSizeButton = true;
		var mapobj = { 
			name: "OSM",
			wms: "osm",
			minzoom: 18,
			maxzoom: 0,
			url: "http://tile.openstreetmap.org/",
			copy:"<a href=\"http://www.openstreetmap.org\" target=\"_blank\">Open Street Map</a>",
			visible:true
		};
		mapTypesArr.push(mapobj);
		var mapobj = { 
			name: "OSM Cycle",
			wms: "osm",
			minzoom: 18,
			maxzoom: 0,
			url: "http://b.tile.opencyclemap.org/cycle/",
			copy:"<a href=\"http://creativecommons.org/licenses/by-sa/2.0/\">Cycle OSM</a>",
			visible:true
		};
		mapTypesArr.push(mapobj);
		var mapobj = { 
			name: "Relief",
			wms: "",
			minzoom: 18,
			maxzoom: 0,
			url: "",
			copy:"<a href=\"http://www.maps-for-free.com/html/about.html\" target=\"_blank\">maps-for-free</a>",
			visible:true
		};
		mapTypesArr.push(mapobj);
		var mapobj = { 
			name: "Demis",
			wms: "wms",
			minzoom: 13,
			maxzoom: 1,
			url: "http://www2.demis.nl/wms/wms.ashx?Service=WMS&WMS=BlueMarble&Version=1.1.0&Request=GetMap&Layers=Earth Image,Borders,Coastlines&Format=image/jpeg",
			copy:"WMS demo by Demis",
			visible:true
		};
		mapTypesArr.push(mapobj);
		var mapobj = { 
			name: "ROADMAP",
			wms: "",
			minzoom: 13,
			maxzoom: 10,
			url: "",
			copy:"",
			visible:true
		};
		mapTypesArr.push(mapobj);
		var mapobj = { 
			name: "SATELLITE",
			wms: "",
			minzoom: 13,
			maxzoom: 10,
			url: "",
			copy:"",
			visible:true
		};
		mapTypesArr.push(mapobj);
		var mapobj = { 
			name: "HYBRID",
			wms: "",
			minzoom: 13,
			maxzoom: 10,
			url: "",
			copy:"",
			visible:true
		};
		mapTypesArr.push(mapobj);
		var mapobj = { 
			name: "TERRAIN",
			wms: "",
			minzoom: 13,
			maxzoom: 10,
			url: "",
			copy:"",
			visible:true
		};
		mapTypesArr.push(mapobj);
		var msg_00 = "click to full size";
		var msg_01 = "IE 8 or higher is needed / switch of compatibility mode";
		var msg_03 = "Distance";
		var msg_04 = "Height";
		var msg_05 = "Download";
		var pluri = "http://www.cesbio.ups-tlse.fr/multitemp/wp-content/plugins/google-maps-gpx-viewer/";
		var ieX = false;
		if (window.navigator.appName == "Microsoft Internet Explorer") {
			var err = ieX = true;
			if (document.documentMode > 7) err = false;
			if(err){
				//alert(msg_01);
			}
		}		

  		
  var map_1 ; 
  var bounds;
  var siteBounds;
  //var groundOverlay;
  var cycleImg = 0;
  var xpos = 100;
  var ypos = 100;
  var overlays = [];
  var imagedata = [];
  var imgOverlaysVisible = true;
  var kml_map;
  var kmlfiles = [];
  var kmloverlays = [];
  var kmlOverlaysVisible = true;
  var latestImage;
  //var overlayOpts = { opacity:0.75, preserveViewport:true }
  var overlayOpts = { preserveViewport:true }
  var pointSW;
  var pointNE;
  var xsize = 520;
  var ysize = 760;

  function setView(site)
  {
     //var lims = [ [-30,-100,50,100] ];
     //var pointSW = new google.maps.LatLng(lims[site][0],lims[site][1]);
     //var pointNE = new google.maps.LatLng(lims[site][2],lims[site][3]);
     //siteBounds = new google.maps.LatLngBounds(pointSW,pointNE);
     //map_1.fitBounds(siteBounds);
  }
  
  function setLatLonView(minLat,minLon,maxLat,maxLon)
  {
     var pointSW = new google.maps.LatLng(minLat,minLon);
     var pointNE = new google.maps.LatLng(maxLat,maxLon);
     siteBounds = new google.maps.LatLngBounds(pointSW,pointNE);
     map_1.fitBounds(siteBounds);    
  }
  
  function setImageOpacity(image)
  {
      var groundOverlay = new google.maps.GroundOverlay( image, bounds, overlayOpts) ;
      groundOverlay.preserveViewport = true;
      groundOverlay.setMap(map_1);
      overlays.push(groundOverlay);
  }

  function cycleImageOverlays(dir)
  {
    cycleImg+=dir;
    if (cycleImg>=overlays.length)
       cycleImg = 0;
    else if (cycleImg<0)
       cycleImg = overlays.length-1;
   
    for (i in overlays) 
    {
      if (i!=cycleImg)
         overlays[i].setMap(null);
      else
         overlays[i].setMap(map_1);
    }
    document.getElementById('data').value = imagedata[cycleImg];
    //document.getElementById('maplabel').innerHTML = "Image " + cycleImg;
    //document.getElementById('maplabel').innerHTML = $data + ' Image ' + cycleImg + ' for year ' + $year + ', day ' +  $day;
  }

  var infowindow = new google.maps.InfoWindow();
  var savcsv="false"; 
  var savkml="false"; 
  var savtext=""; 
  var infowinopts = '<div id="myInfoWinDiv">'
  + '<input type="checkbox" id="opt1" value="'+savcsv+'">CSV'
  + '<input type="checkbox" id="opt2" value="'+savkml+'">KML'
  + '<input type="text" id="text" value="'+savtext+'">'
  + '<input type="button" onclick="saveButton()" name="save" value="Save">'
  + '</div>';

  function saveButton()
  {
     savcsv = document.getElementById('opt1').checked;
     savkml = document.getElementById('opt2').checked;
     savtext = document.getElementById('text').value;
     
     var fileName = document.getElementById('param').value
     var dotpos = fileName.lastIndexOf(".");
     var ulpos = fileName.lastIndexOf("_"); 
     if (ulpos>dotpos) dotpos = ulpos;
     var rootname = fileName.substring(7,dotpos);
     var AoI = fileName.substring(dotpos+1,fileName.length);

     var csvName="NULL";
     var csvchecked="";
     var usetext = savtext;
     var savmode = 0;
     if (savtext!="") usetext=savtext+"_";
     if (savcsv==true)
     {
     	 csvchecked="checked";
     	 csvName = usetext+rootname+"_"+AoI;
     	 savmode+=1;
     }
     var kmlName="NULL";
     var kmlchecked="";
     if (savkml==true)
     {
     	 kmlchecked="checked";
     	 kmlName = usetext + AoI;
     	 savmode+=2;
     }
     
     var xmlhttp = new XMLHttpRequest();
//     xmlhttp.open("GET", "infowin.php?q=" + csvName + "&r=" + kmlName, true); 
     console.log("infowin: " + savtext + "&r=" + AoI + "&s=" + savmode);
     xmlhttp.open("GET", "infowin.php?q=" + savtext + "&r=" + AoI + "&s=" + savmode, true); 
     xmlhttp.send(); 
     
     infowinopts = '<div id="myInfoWinDiv">'
     + '<input type="checkbox" id="opt1" '+csvchecked+' >CSV '
     + '<input type="checkbox" id="opt2" '+kmlchecked+' >KML '
     + '<input type="text" id="text" value="'+savtext+'">'
     + '<input type="button" onclick="saveButton()" name="save" value="Save">'
     + '</div>';     
     infowindow.close();
  }
  
  var x = null;        
  
  function addKMLfile(kmlfile)
  {  	
     kmlfiles.push(kmlfile);
  }
  
  function addKMLoverlay(kmlfile)
  {
  	//window.alert("Adding KML file:"+kmlfile);
	kml_map = new google.maps.KmlLayer(kmlfile,{preserveViewport:true});
	kml_map.preserveViewport = true;
	kml_map.setOptions({suppressInfoWindows: true});
	kml_map.setMap(map_1);
	//kml_map.author = kmlfile;
	//kml_map.author.uri = kml_map.url;
	
	google.maps.event.addListener(kml_map,'click', function(event) {
          console.log("KML click: name="+event.featureData.name);
          var kmlFileName = event.featureData.description;
          console.log("KML click: descrip="+kmlFileName);
          //console.log("KML click:URL="+event.featureData.author.uri);
          var llMid = event.latLng;

               var fileName = document.getElementById('param').value + '.tif';
               var xmlpolyhttp = new XMLHttpRequest();
                xmlpolyhttp.onreadystatechange = function() 
                {
                    if (xmlpolyhttp.readyState == 4 && xmlpolyhttp.status == 200) 
                    {
                         //console.log("Poly info:"+xmlpolyhttp.responseText);
                         var names=optlist.split(',');      
                         var vals=xmlpolyhttp.responseText.split(';');  
                         //var msg = 'Area Information<br><table><tr><td width="150">Attribute</td><td width="60">Area</td><td width="60">Mean</td><td width="60">Stdev</td><td width="60">Min</td width="60"><td>Max</td></tr>';
                         var msg = 'Area Information<br><table><tr><td width="150">Attribute</td><td width="60">Area</td><td width="60">PerHa</td><td width="60">Total</td></tr>';
                         for (var ii=0;ii<names.length-1;ii++)
                         {                         	 
                            msg = msg + '<tr><td>' + names[ii] + '</td>'; 
                            var cols=vals[ii].split(','); 
                            for (var jj=0;jj<cols.length;jj++)
                               msg = msg + '<td>' +  cols[jj] + '</td>';
                            msg = msg + '</tr>';
                         }
                         msg = msg + '</table>';
                         infowindow.setPosition(llMid);
                         var contents = msg + "<br>" +infowinopts;
                         infowindow.setContent(contents);
                         infowindow.open(map_1);
                    }
                };
                if ((optlist.indexOf(",")>0) && (optlist.indexOf(",")<optlist.length-2))
                {
        	        //fileName=fileName+","+optlist; // pass list of names!
        	        fileName=RootPath+"/images/*."+selRegion+".tif,"+optlist; // pass list of names!
                }
                console.log("Getting polygon info for "+fileName+", kmlKileName="+kmlFileName);
                xmlpolyhttp.open("GET", "TifPolyAreaVal.php?q=" + fileName + "&r=0&s=0&t=" + kmlFileName, true); 
                xmlpolyhttp.send();         
         });
	kmloverlays.push(kml_map);
  }

function toggleKmlOverlays()
{
   if (kmlOverlaysVisible)
   {
      for (i in kmloverlays) kmloverlays[i].setMap(null);
      kmlOverlaysVisible = false;
      //unset(kmloverlays);
      //window.alert("Hide polygons");
   }
   else
   {
      //window.alert("Show polygons");
      for (i in kmloverlays)
      {
	      kmloverlays[i].preserveViewport = true;
      	  kmloverlays[i].setMap(map_1);
      }
      kmlOverlaysVisible = true;
   }
}

function addKMLoverlays()
{	
   kmlOverlaysVisible = true;

   <?php
   $actual_link = 'http://'.$_SERVER['HTTP_HOST'];
   if ($RootPath==".")
      $kmlpath = $actual_link . "/GSiMaps/kml/";
   else
      $kmlpath = $actual_link . "/GSiMaps/".$RootPath."/kml/";  
   echo "console.log('kmlpath=".  $kmlpath . "');\n"; 
   $block = substr($pngrefile, -2);
   $kmlfile = $kmlpath."Harvest_Wagner".$block.".kml";
   echo "addKMLoverlay('" . $kmlfile . "');\n";
   ?>
}
  
  function PlotMap()
  {
	google.setOnLoadCallback(function() {		
	
	map_1 = init_map("SATELLITE", "map_1", 0);
	init_slider();
	setView(0);

    var LatLonHTML='<td>Lat: <input type="text" id="latitude" style="width: 80px;" placeholder="latitude"> </td><td>Lon: <input type="text" id="longitude" style="width: 80px;" placeholder="longitude"> </td>';
    var MultiFileHTML='<td> Data: <input type="button" value="&#9664" onclick="cycleImageOverlays(-1);" /></td><td><input type="text" id="data" style="left: 600px; width: 180px;" placeholder="data"></td><td><input type="button" value="&#x25b6" onclick="cycleImageOverlays(1);" /></td>';
    var InfoHTML = LatLonHTML + MultiFileHTML;
<?php
 //  if ($DisplayMode=="4")
/*
   {
      echo 'InfoHTML = LatLonHTML + MultiFileHTML';
   }
*/
?>

    var myTitle = document.createElement('h1');
    myTitle.style.color = 'white';
    myTitle.style.fontSize = "small";
    myTitle.style.fontWeight = "normal";
    myTitle.innerHTML = InfoHTML;
    var myTextDiv = document.createElement('div');
    myTextDiv.appendChild(myTitle);

    map.controls[google.maps.ControlPosition.BOTTOM_CENTER].push(myTextDiv);	
	
	load_map(map_1, "", "", "");
	//document.getElementById('map_1').style.width = window.innerWidth;
	//document.getElementById('map_1').style.height = window.innerHeight;
	
	map_1["elevation"] = true; 
	map_1["download"] = true; 
	map_1.g_seCookie = false; // no cookie
	map_1.g_showCnt++;
				
	var fileName = document.getElementById('param').value + '.tif';

	var selectedShape;

   function clearSelection() {
   	 console.log("clearSelection called");
     if (selectedShape) {
       console.log("Selected shape was set");
       selectedShape.setEditable(false);
       selectedShape = null;
     }
   }

	var drawingManager = new google.maps.drawing.DrawingManager({
//		drawingMode: google.maps.drawing.OverlayType.POLYGON,
		drawingControl: true,
		drawingControlOptions: {
		position: google.maps.ControlPosition.TOP_CENTER,
		drawingModes: [
			google.maps.drawing.OverlayType.POLYGON,
			google.maps.drawing.OverlayType.RECTANGLE
			]
		},
		polygonOptions: {
                  strokeColor: '#ffff00',
                  fillColor: '#ffff00',
                  fillOpacity: 0.5,
                  strokeWeight: 2,
                  clickable: false,
                  editable: false,
                  zIndex: 1
                },
		rectangleOptions: {
                  strokeColor: '#ffff00',
                  fillColor: '#ffff00',
                  fillOpacity: 0.5,
                  strokeWeight: 2,
                  clickable: false,
                  editable: false,
                  zIndex: 1
                }

	});
	

  if (AllowDrawing==1)
  {
	drawingManager.setMap(map_1);
	setView(0);		
  
	google.maps.event.addListener(drawingManager, 'rectanglecomplete', function(rectangle) {
		selectedShape = rectangle;
		var bounds = rectangle.getBounds();
		llNE = bounds.getNorthEast();
		llSW = bounds.getSouthWest(); 
		midlat = ( llSW.lat() + llNE.lat() ) / 2.0;
		midlon = ( llSW.lng() + llNE.lng() ) /2.0;
		var llMid = new google.maps.LatLng(midlat,midlon);
		
                var polylon = llNE.lng()+","+llNE.lng()+","+llSW.lng()+","+llSW.lng()+","+llNE.lng();
                var polylat = llNE.lat()+","+llSW.lat()+","+llSW.lat()+","+llNE.lat()+","+llNE.lat();

                var fileName = document.getElementById('param').value + '.tif';
                
		//alert("Rectangle drawn: "+llSW.lat()+","+llSW.lng()+" to "+llNE.lat()+","+llNE.lng());
                var xmlpolyhttp = new XMLHttpRequest();
                xmlpolyhttp.onreadystatechange = function() 
                {
                    if (xmlpolyhttp.readyState == 4 && xmlpolyhttp.status == 200) 
                    {
                         //console.log("Rectangle info:"+xmlpolyhttp.responseText);
                         var names=optlist.split(',');      
                         var vals=xmlpolyhttp.responseText.split(';');  
                         //var msg = 'Area Information<br><table><tr><td width="150">Attribute</td><td width="60">Area</td><td width="60">Mean</td><td width="60">Stdev</td><td width="60">Min</td width="60"><td>Max</td></tr>';
                         var msg = 'Area Information<br><table><tr><td width="150">Attribute</td><td width="60">Area</td><td width="60">PerHa</td><td width="60">Total</td></tr>';
                         for (var ii=0;ii<names.length-1;ii++)
                         {
                             msg = msg + '<tr><td>' + names[ii] + '</td>'; 
                            var cols=vals[ii].split(','); 
                            for (var jj=0;jj<cols.length;jj++)
                               msg = msg + '<td>' +  cols[jj] + '</td>';
                            msg = msg + '</tr>';
                         }
                         msg = msg + '</table>';
                         infowindow.setPosition(llMid);
                         var contents = msg + "<br>" +infowinopts;
                         infowindow.setContent(contents);
                         infowindow.open(map_1);
                    }
                };
                if ((optlist.indexOf(",")>0) && (optlist.indexOf(",")<optlist.length-2))
                {
        	        //fileName=fileName+","+optlist; // pass list of names!
        	        fileName=RootPath+"/images/*."+selRegion+".tif,"+optlist; // pass list of names!
                }
               //window.alert("Getting polygon info for "+fileName);
                xmlpolyhttp.open("GET", "TifPolyAreaVal.php?q=" + fileName + "&r=" + polylat + "&s=" + polylon, true); 
                xmlpolyhttp.send(); 		
	});

	google.maps.event.addListener(drawingManager, 'polygoncomplete', function(polygon) {
		selectedShape = polygon;
		var bounds = new google.maps.LatLngBounds();
		var paths = polygon.getPaths();
		var path;
                var polylon = "";
                var polylat = "";
                
                var fileName = document.getElementById('param').value + '.tif';

		for (var p = 0; p < paths.getLength(); p++) {
		    path = paths.getAt(p);
		    for (var i = 0; i < path.getLength(); i++) {
                        polylon = polylon + path.getAt(i).lng();
                        if (i < path.getLength()-1) polylon = polylon +  ",";
                        polylat = polylat + path.getAt(i).lat();
                         if (i < path.getLength()-1) polylat = polylat +  ",";
		    	bounds.extend(path.getAt(i));
		    }
		}
		llNE = bounds.getNorthEast();
		llSW = bounds.getSouthWest();  
		//ll_lims = llSW.lat()+","+llSW.lng()+" to "+llNE.lat()+","+llNE.lng();
		midlat = ( llSW.lat() + llNE.lat() ) / 2.0;
		midlon = ( llSW.lng() + llNE.lng() ) /2.0;
		var llMid = new google.maps.LatLng(midlat,midlon);

		//alert("Polygon drawn: "+llSW.lat()+","+llSW.lng()+" to "+llNE.lat()+","+llNE.lng());
                //alert("PolyLon = "+polylon);
                //alert("PolyLat = "+polylat);
                
                var xmlpolyhttp = new XMLHttpRequest();
                xmlpolyhttp.onreadystatechange = function() 
                {
                    if (xmlpolyhttp.readyState == 4 && xmlpolyhttp.status == 200) 
                    {
                         //console.log("Poly info:"+xmlpolyhttp.responseText);
                         var names=optlist.split(',');      
                         var vals=xmlpolyhttp.responseText.split(';');  
                        // var msg = 'Area Information<br><table><tr><td width="150">Attribute</td><td width="60">Area</td><td width="60">Mean</td><td width="60">Stdev</td><td width="60">Min</td width="60"><td>Max</td></tr>';
                         var msg = 'Area Information<br><table><tr><td width="150">Attribute</td><td width="60">Area</td><td width="60">PerHa</td><td width="60">Total</td></tr>';
                         for (var ii=0;ii<names.length-1;ii++)
                         {
                         	 
                            msg = msg + '<tr><td>' + names[ii] + '</td>'; 
                            var cols=vals[ii].split(','); 
                            for (var jj=0;jj<cols.length;jj++)
                               msg = msg + '<td>' +  cols[jj] + '</td>';
                            msg = msg + '</tr>';
                         }
                         msg = msg + '</table>';
                         infowindow.setPosition(llMid);
                         var contents = msg + "<br>" +infowinopts;
                         infowindow.setContent(contents);
                         infowindow.open(map_1);
                    }
                };
                if ((optlist.indexOf(",")>0) && (optlist.indexOf(",")<optlist.length-2))
                {
        	        //fileName=fileName+","+optlist; // pass list of names!
        	        fileName=RootPath+"/images/*."+selRegion+".tif,"+optlist; // pass list of names!
                }
                console.log("Getting polygon info for "+fileName);
                xmlpolyhttp.open("GET", "TifPolyAreaVal.php?q=" + fileName + "&r=" + polylat + "&s=" + polylon, true); 
                xmlpolyhttp.send();  
	});
	
    google.maps.event.addListener(drawingManager, 'drawingmode_changed', clearSelection);
    google.maps.event.addListener(map_1, 'click', clearSelection);	
  }

	addKMLoverlays();
	addImageOverlays();

//	if (document.getElementById('data')!=null)
//	{
//   	   window.alert("try setting data to "+imagedata[0]);
//   	   document.getElementById('data').value = imagedata[0];
//	}
	
	post_init(map_1);

        var logoControlDiv = document.createElement('DIV');
        var logoControl = new MyLogoControl(logoControlDiv);
        logoControlDiv.index = 0; // used for ordering
        map_1.controls[google.maps.ControlPosition.BOTTOM_LEFT].push(logoControlDiv);
	
	});
  }
 
  function DEMdisplay(ovlroot)
  {
  	  /*
                var demhttp = new XMLHttpRequest();
                demhttp.onreadystatechange = function() 
                {
                    if (demhttp.readyState == 4 && demhttp.status == 200) 
                    {
                         var demresponse=demhttp.responseText;  
                    }
                };
       */         
        	    var demName=RootPath+"/DEM/DEM."+selRegion+".bin";
                //var ovlName=RootPath+"/DEM/"+ovlroot+"."+selRegion+".jpg";
                var ovlName;
                if (ovlroot.indexOf("png")>=0)
                   ovlName=ovlroot+"."+selRegion+".png";
                else
                   ovlName=ovlroot+"."+selRegion+".jpg";
                var callURL="3DTerrain.php?dem=" + demName + "&ovl=" +ovlName;

                console.log("Starting 3D Terrain for "+callURL);
                window.open(callURL);
                
                //demhttp.open("GET", "3DTerrain.php?dem=" + demName + "&ovl=" +ovlName, true); 
                //demhttp.send();  
  }
  
<?php

//require_once 'MMGeoTIFFReader.php';  //MM 16Jun16

    $pngminlat = 0;
    $pngmaxlat = 0;
    $pngminlon = 0;
    $pngmaxlon = 0;
    
    function getGeoTiffInfo($fileName) {
        global $pngminlat,$pngmaxlat,$pngminlon,$pngmaxlon;
        
        // standard TIFF constants
        $TIFF_ID = 42;             // magic number located at bytes 2-3 which identifies a TIFF file
        $TAG_STRIPOFFSETS = 273;   // identifying code for 'StripOffsets' tag in the Image File Directory (IFD)
        $TAG_IMAGE_WIDTH = 256;
        $TAG_IMAGE_LENGTH = 257;      
        $LEN_IFD_FIELD = 12;       // the number of bytes in each IFD entry
        $BIG_ENDIAN = "MM";        // byte order identifiers located at bytes 0-1
        $LITTLE_ENDIAN = "II";        
        $TAG_SCALE  = 33550;       // Xscale, Yscale (doubles)
        $TAG_LOCATION  = 33922;    // Top Left Lat, Lon (doubles)
        $TAG_ResolutionUnit  = 296;
        $TAG_XResolution     = 282;
        $TAG_YResolution     = 283;
        $TAG_Orientation     = 274;
        $TAG_XPosition       = 286;
        $TAG_YPosition       = 287;
           
        $fp = fopen($fileName, 'rb');
                          
        // go to the file header and work out the byte order (bytes 0-1) 
        // and TIFF identifier (bytes 2-3) 
        fseek($fp, 0);
        $dataBytes = fread($fp, 4);
        $data = unpack('c2chars/vTIFF_ID', $dataBytes);
        
        // check it's a valid TIFF file by looking for the magic number  
        $TIFF = $data['TIFF_ID'];        
        
        // convert the byte order code to ASCII to get Motorola or Intel ordering identifiers
        $byteOrder = sprintf('%c%c', $data['chars1'], $data['chars2']);        
        
        // the remaining 4 bytes in the header are the offset to the IFD
        fseek($fp, 4);
        $dataBytes = fread($fp, 4);
        // unpack in whichever byte order was identified previously 
        // - this seems to be always 'II' but whether this is always the case is not specified
        // so we do the check each time to make sure
        if ($byteOrder == $LITTLE_ENDIAN) { 
            $data = unpack('VIFDoffset', $dataBytes); 
        }
        elseif ($byteOrder == $BIG_ENDIAN){
            $data = unpack('NIFDoffset', $dataBytes);
        }
        
        // now jump to the IFD offset and get the number of entries in the IFD
        // which is always stored in the first two bytes of the IFD
        fseek($fp, $data['IFDoffset']);
        $dataBytes = fread($fp, 2) ;
        $data = ($byteOrder == $LITTLE_ENDIAN) ? 
            unpack('vcount', $dataBytes) : 
            unpack('ncount', $dataBytes);   
        $numFields = $data['count'];
        
        // iterate the IFD entries until we find the ones we need 
        for ($i = 0; $i < $numFields; $i++) {
            $dataBytes = fread($fp, $LEN_IFD_FIELD);
            $data = ($byteOrder == $LITTLE_ENDIAN) ? 
                unpack('vtag/vtype/Vcount/Voffset', $dataBytes) : 
                unpack('ntag/ntype/Ncount/Noffset', $dataBytes);
            // echo 'Field: ' . $data['tag'] . "<br>\n";    
            switch($data['tag']) {
                case $TAG_IMAGE_WIDTH :
                    $numDataCols = $data['offset'];
                    break;
                case $TAG_IMAGE_LENGTH :
                    $numDataRows = $data['offset'];
                    break;                    
                case $TAG_STRIPOFFSETS : 
                    $stripOffsets = $data['offset'];
                    break;
                case $TAG_SCALE : 
                    $ScalePos = $data['offset'];
                    break; 
                case $TAG_LOCATION : 
                    $LocnPos = $data['offset'];
                    break;
            } 
        }
        $xw = $numDataCols;
        $yw = $numDataRows;
        
        fseek($fp, $ScalePos);
        $dataBytes = fread($fp, 16) ;
        $dval = unpack('d2val', $dataBytes);
        
        fseek($fp, $LocnPos);
        $dataBytes = fread($fp, 48) ;
        $locval = unpack('d6val', $dataBytes);
        $pngmaxlat = $locval['val5'];
        $pngminlon = $locval['val4'];
        $pngmaxlon = $locval['val4']+$xw*$dval['val1'];
        $pngminlat = $locval['val5']-$yw*$dval['val2'];
    }
?>


// Main APIs for adding to map
function addImageOverlays()
{
   <?php
   global $pngminlat,$pngmaxlat,$pngminlon,$pngmaxlon;
   //$pngrefile = $_REQUEST["q"];
   $pngminlat = $_REQUEST["r"];
   $pngminlon = $_REQUEST["s"];
   $pngmaxlat = $_REQUEST["t"];
   $pngmaxlon = $_REQUEST["u"];
   
   $tifile=$pngrefile.".tif";
   if (file_exists($tifile))
   {
      echo "//File exists: ".$tifile."\n";
   }
   else
   {
      echo "//File does not exist: ".$tifile."\n";
      //echo "overlays = [];\n";
   }
   
   if ($pngrefile!=null)
   {
      if ($pngmaxlon!=null)
      {
      	  $pngfile = $pngrefile;
      }
      else // Assume filename specified without suffix, as we want to check tif and png files
      {
      	  if (fnmatch('*h??v??*',$pngrefile))
      	  {
      	     // looks like a MODIS tile! So Calc min/max lat lon
      	     //echo "Looks like MODIS tile<br>\n";
      	     $ioff = 0;
      	     $hpos = strpos($pngrefile,"h",$ioff);
      	     $match = 0;
      	     while (($hpos!=null) && ($match==0))
      	     {
      	        $vpos = strpos($pngrefile,"v",$hpos);
      	        if ($vpos==null) $vpos = $hpos+1;
      	       // echo 'hpos=' . $hpos . ' vpos=' . $vpos . "<br>\n";
      	        if (($vpos-$hpos)==3)
      	        {
      	     	    //echo "Found hXxvYY<br>\n";
      	     	    $match = 1;
      	        }
      	        else
      	        {
      	            //echo "Found h and/or v, but not in right place<br>\n";	
      	            $hpos = strpos($pngrefile,"h",$hpos+1);
      	        }
      	     }
      	     
      	     if ($match>0) // This is definitely a MODIS tile geotiff
      	     {
      	         $hh = substr($pngrefile,$hpos+1,2);
      	         $vv = substr($pngrefile,$vpos+1,2);
      	     	 $pngmaxlat = 90 - ($vv+0)*10;
      	     	 $pngminlat = $pngmaxlat - 10;
      	     	 $londegW = ($hh+0)*10-180;
      	     	 $londegE = $londegW + 10;
      	     	 $rminlat = deg2rad($pngminlat);
      	     	 $rmaxlat = deg2rad($pngmaxlat);
      	     	 $lonW = $londegW/cos($rminlat);
      	     	 $lonW2 = $londegW/cos($rmaxlat);
      	     	 if ($lonW2<$lonW) $lonW=$lonW2;
      	     	 $lonE = $londegE/cos($rminlat);
      	     	 $lonE2 = $londegE/cos($rmaxlat);
      	     	 if ($lonE2>$lonE) $lonE=$lonE2;
                 $pngminlon = $lonW;
                 $pngmaxlon = $lonE;
      	     }
      	     else
                getGeoTiffInfo($pngrefile . '.tif');
      	  }
      	  else
             getGeoTiffInfo($pngrefile . '.tif');
 
          $pngfile = 'MapDisplay.png';
          // Allow for pre-set png file in png/*
          $presetpngfile = str_replace("images","png",$pngrefile) . '.png';
          if (file_exists($presetpngfile))
          {
             $pngfile = $presetpngfile;
          }
      }
      //echo 'MinLon=' . $pngminlon . ' MaxLon=' . $pngmaxlon . "<br>\n";
      //echo 'MinLat=' . $pngminlat . ' MaxLat=' . $pngmaxlat . "<br>\n";
      if (($DisplayMode!="4") && (file_exists($tifile)))
      {
         //echo 'window.alert("orig pngfile='.$pngfile.' minlat='.$pngminlat.' pngrefile='.$pngrefile.'");';
         echo "addImage('" . $pngfile . "'," . $pngminlat . "," . $pngminlon . "," . $pngmaxlat . "," . $pngmaxlon . ");\n";
         echo 'document.getElementById("param").value = "' . $pngrefile . '";' . "\n";
         //echo 'document.getElementById("data").value =  "' . $pngrefile . '";' . "\n";
         $lastpos=strpos($pngrefile,".");
         $dataname=substr($pngrefile,7,$lastpos-7);
         echo "imagedata[0] = '" . $dataname . "';\n";
      }
      else
      {
         //$fileWildName="png/Lincoln_2016*_NewNDVI_10m_Mask.png";
         //$fileWildName="png/HeightLidarObs_*OneScene.png";
         $fileWildName=$RootPath."/png/".$RootWildFileName.".png";
         //echo 'window.alert("'.$fileWildName.'");';
         $count=0;
         foreach (glob($fileWildName) as $pngfile) {
            //echo 'window.alert("'.$fileName.'");';
            //$pngfile = str_replace("images","png",$fileName) . '.png';	 
            $EndWildPos = strpos($pngfile,$WildRemaining); 
            echo "addImage('" . $pngfile . "'," . $pngminlat . "," . $pngminlon . "," . $pngmaxlat . "," . $pngmaxlon . ");\n";
            $StartPos=strrpos($pngfile,"/")+1;
            $name=substr($pngfile,$StartPos,$EndWildPos-$StartPos);
            echo "imagedata[" . $count ."] = \"". $name. "\";\n";
            //echo 'console.log("imagedata['.$count.'] = '.$name.'");'."\n";
            echo "document.getElementById('".$name."').checked = true;\n";
//            echo "optlist=optlist+".$name."+',';\n";
            //echo "addImage('" . $pngfile . "'," . $pngminlat . "," . $pngminlon . "," . $pngmaxlat . "," . $pngmaxlon . ");\n";
            //echo "imagedata[" . $count ."] = \"". substr($pngfile,19,5). "\";\n";
            $count++;
         }
         echo 'document.getElementById("param").value = "' . $pngfile . '";' . "\n";    
//         echo "console.log('optlist='+optlist);\n";
         //echo 'document.getElementById("data").value = "' . substr($pngfile,$StartWildPos,$EndWildPos-$StartWildPos) . '";' . "\n";     	      
      }      
   }
/*   
   else if (!empty($_POST))
   {
      for ($img=1;$img<$linenum;$img++)
      {
   	$name = "cb_" . $img;
	if (isset($_POST[$name]))
	{
		echo "addImage('" . $imgline[$img][10] . "'," . $imgline[$img][6] . "," . $imgline[$img][5] . "," . $imgline[$img][8] . "," . $imgline[$img][7] . ");\n";
                echo 'document.getElementById("param").value = "' . $imgline[$img][9] . '";' . "\n";
	}
      }
      
   }
*/   
   ?>
}

function toggleImageOverlays()
{
   if (imgOverlaysVisible)
   {
      for (i in overlays) overlays[i].setMap(null);
       imgOverlaysVisible = false;
   }
   else
   {
      //for (i in overlays) overlays[i].setMap(map_1);
      for (i in overlays) 
      {
        if (i!=cycleImg)
         overlays[i].setMap(null);
        else
         overlays[i].setMap(map_1);
      }
      imgOverlaysVisible = true;
   }
}


function addImage(image,minlat,minlon,maxlat,maxlon)
{
   //window.alert("Adding image file:"+image);

   var multipixfname = "MergeTif_Scale10.bin";
   var pointSW = new google.maps.LatLng(minlat,minlon);
   var pointNE = new google.maps.LatLng(maxlat,maxlon);
   bounds = new google.maps.LatLngBounds(pointSW,pointNE);
   if (new_region==1) map_1.fitBounds(bounds);
   new_region = 0;
   
   //var groundOverlay = new google.maps.GroundOverlay( image, bounds, overlayOpts) ; // overlayOpts defines opacity
   var groundOverlay = new google.maps.GroundOverlay( image, bounds ,{preserveViewport:true});
   
//   var overlayoptions={ backgroundColor: 'hsla(0, 0, 0, 0)' };
//   groundOverlay.setOptions(overlayoptions);
   groundOverlay.preserveViewport = true;
   map_1.preserveViewport = true;
   groundOverlay.setMap(map_1);
//   groundOverlay.setOptions(overlayoptions);
    
   overlays.push(groundOverlay);
   latestImage = image;
   
   var x = 100;
   var y = 100;
   var pixel = 123; //ctx.getImageData(x, y, 1, 1).data;
   var contentString;
   
    var lat = document.getElementById('latitude');
    var lon = document.getElementById('longitude');
    var latlon;
    
    if (lat!=0)
       latlon = new google.maps.LatLng(lat, lon);
    else
       latlon = new google.maps.LatLng((minlat+maxlat)/2, (minlon+maxlon)/2);
    var MMmarker = null;
      
      var xsize = 520;
      var ysize = 760;
      
      google.maps.event.addListener(groundOverlay, 'mousemove', function (event) 
      {
      	var lat = event.latLng.lat();
      	var lon = event.latLng.lng();
        xpos = xsize*(lon - minlon)/(maxlon-minlon);
        if (xpos<0) xpos=0;
        if (xpos>=xsize) xpos=xsize-1;
        ypos = ysize*(maxlat - lat)/(maxlat-minlat);
        if (ypos<0) ypos=0;
        if (ypos>=ysize) ypos=ysize-1;
        document.getElementById('latitude').value = lat.toFixed(6);
        document.getElementById('longitude').value = lon.toFixed(6);
      });

      var infowindow = new google.maps.InfoWindow();
      var x = null;      
      
      google.maps.event.addListener(groundOverlay, 'click', function (event) {

      	var lat = event.latLng.lat();
      	var lon = event.latLng.lng();
        xpos = xsize*(lon - minlon)/(maxlon-minlon);
        if (xpos<0) xpos=0;
        if (xpos>=xsize) xpos=xsize-1;
        ypos = ysize*(maxlat - lat)/(maxlat-minlat);
        if (ypos<0) ypos=0;
        if (ypos>=ysize) ypos=ysize-1;
        
        chart = 0;
        if (document.getElementById('chart').value != null)
        {
           chart = document.getElementById('chart').value;
        }
        
        var fileName = document.getElementById('param').value + '.tif';
        if (document.getElementById('multifile').value != null)
        {
           if (document.getElementById('multifile').value.length>1)
           {
              fileName = document.getElementById('multifile').value + ".tif";
           }
           else
              chart = 0;
        }
        else
           chart = 0;
           
        //console.log("mouseclick: fileName="+fileName+", optList: "+optlist);
/* Now test for being inside a polygon
      var xmlpolyhttp = new XMLHttpRequest();
      xmlpolyhttp.onreadystatechange = function() 
      {
            if (xmlpolyhttp.readyState == 4 && xmlpolyhttp.status == 200) 
            {
                 console.log("Poly info:"+xmlpolyhttp.responseText);
                 infowindow.setPosition(event.latLng);
                 var contents = xmlpolyhttp.responseText;
                 infowindow.setContent(contents);
                 infowindow.open(map_1);
             }
      };
      //if ((kmllist.indexOf(",")>0) && (kmllist.indexOf(",")<kmllist.length-2))
      //{
        	 fileName=RootPath+"/kml/MMtest2_WagnerB1_0.kml";   // +selRegion+".kml," // +kmllist; // pass list of names!
      //}
      console.log("Getting polygon check for lat="+lat+", lon="+lon+", kml="+fileName);
      xmlpolyhttp.open("GET", "CheckWithinPoly.php?q=" + fileName + "&r=" + lat + "&s=" + lon, true); 
      xmlpolyhttp.send();        
*/       
      var checkpoint=1;
      if (checkpoint==1)
      {
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function() 
        {
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200) 
            {
              if (chart==0)
              {
<?php
                  if ($DisplayMode=="1")
                  {
                     echo "var msg = '<p>Height = '+parseInt(xmlhttp.responseText)/10+' metres</p>'\n";
                  }
                  //else if ($DisplayMode=="4")
                  //{
                  //   echo "var msg = '<p>Heights (1/10th metres): '+xmlhttp.responseText+'</p>'\n";
                  //}
                  else
                  {
                     //echo "var msg = '<p>Pixval = '+xmlhttp.responseText+'</p>'\n";
                     echo "var msg = '';";
                     echo "var names=optlist.split(',');  \n";      
                     echo "var vals=xmlhttp.responseText.split(',');  \n";   
                     echo "for (var ii=0;ii<names.length-1;ii++)\n";
                     echo "   msg = msg + names[ii] + ' : ' + vals[ii]+ '<br>';\n";
                     //echo "var msg = optlist + '<br>'+ xmlhttp.responseText + '<br>'\n";
                  }
?>
                  contentString = '<div id="bodyContent">'+
//                 '<p><b>Pixel Information</b></p>'+
                 '<p>Lat = '+lat.toFixed(6)+'  Lon = '+lon.toFixed(6)+'</p>'+ msg +
//                 '<p>Pixval ='+xmlhttp.responseText+'</p>'+
                 '</div>';
                      
                 infowindow.setPosition(event.latLng);
                 infowindow.setContent(contentString);
                 infowindow.open(map_1);
              }
              else // plot chart
              {
              	 if (x!=null) x.close();      
              	 x = window.open('','','width=420, height=320');
                 x.document.open();
                 x.document.write(xmlhttp.responseText);
                 x.document.close();
              }
           }
        };
        if ((optlist.indexOf(",")>0) && (optlist.indexOf(",")<optlist.length-2))
        {
        	//fileName=fileName+","+optlist; // pass list of names!
        	fileName=RootPath+"/images/*."+selRegion+".tif,"+optlist; // pass list of names!
        }
        console.log("TifPixVal: "+fileName);
        //console.log("TifPixVal.php?q=" + fileName + "&r=" + lat + "&s=" + lon + "&t=" + chart, true); 
        xmlhttp.open("GET", "TifPixVal.php?q=" + fileName + "&r=" + lat + "&s=" + lon + "&t=" + chart, true); 
        xmlhttp.send();  
      }
    });
      
}

function setOpacity(percent)
{
   var frac = 0.01*percent;
   for (i in overlays) overlays[i].setMap(null);
   overlayOpts.opacity = frac;
   for (i in overlays)  {
      overlays[i].setOpacity(frac);
      //overlays[i].setMap(map_1);
      if (i!=cycleImg)
         overlays[i].setMap(null);
      else
         overlays[i].setMap(map_1);
   }
   imgOverlaysVisible = true; 
   
   <?php
   if (!empty($_POST))
   {
      for ($img=1;$img<$linenum;$img++)
      {
   	$name = "cb_" . $img;
	if (isset($_POST[$name]))
	{
	   echo "addImage('" . $imgline[$img][10] . "'," . $imgline[$img][6] . "," . $imgline[$img][5] . "," . $imgline[$img][8] . "," . $imgline[$img][7] . ");\n";
	}
      }
   }
   ?>
}

function MyLogoControl(controlDiv) {
    controlDiv.style.padding = '5px';
    var logo = document.createElement('IMG');
    logo.src = 'GSIlogo.png';
    logo.style.cursor = 'pointer';
    controlDiv.appendChild(logo);

    google.maps.event.addDomListener(logo, 'click', function() {
        window.location = 'http://www.surfaceintelligence.com'; 
    });
    
}

// Plot Map
PlotMap();

</script>

</body>
</html> 