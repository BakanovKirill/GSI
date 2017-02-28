<?php

/**
*  Returns pixval from GeoTIFF file given WGS84 latitude and Longitude
*/

class MMGeoTIFFReader {

	const LEN_OFFSET = 4;           // the number of bytes required to hold a TIFF offset address

	// CGIAR-CSI SRTM GeoTIFF constants
	const DEGREES_PER_TILE = 5;     // each tile is 5 x 5 degrees of lat/lon
	const PIXEL_DIST = 0.000833333; // the distance represented by one pixel (0 degrees 0 mins 3 secs of arc = 1/1200)
	const NO_DATA = 0x8000;         // data void displays as -32768 (converted to signed short)

	// read/write public properties
	public $showErrors = true;     // show messages on error condition, otherwise dies silently
	public $maxPoints = 5000;      // default maximum number of multiple locations accepted

	// private properties
	private $dataDir;              // path to local directory containing the GeoTIFF data files
	private $fileName;             // name of current GeoTIFF data file
	private $fp;                   // file pointer to current GeoTIFF data file
	private $tileRefHoriz;         // the horizontal tile reference figure (01-72)
	private $tileRefVert;          // the vertical tile reference figure (01-24)
	private $latLons = Array();    // the supplied lats & lons
	private $elevations = Array(); // the elevations values found

	/**
	* Constructor: assigns data directory
	*
	* @param mixed $dataDir
	* @return SRTMGeoTIFFReader
	*/
	function __construct($dataDir) {
		$this->dataDir = $dataDir;
	}

	/**
	* Destructor: clean up resources
	*
	*/
	function __destruct() {
		if ($this->fp) {
			fclose($this->fp);
		}
	 }

	/**
	* Returns the current file name
	*/
	public function getFileName() {
		return $this->fileName;
	}
/*
   function debug_to_console( $data ) {

	if ( is_array( $data ) )
		$output = "<script>console.log( 'Debug Objects: " . implode( ',', $data) . "' );</script>";
	else
		$output = "<script>console.log( 'Debug Objects: " . $data . "' );</script>";

	echo $output;
   }
*/
	/*
	* Convert geotiff to png at reduced scale, using specified LUT
	*/
	public function TifToPng($fileName, $reduce, $LUTfile) {
	   $pngminlat = 0;
	   $pngmaxlat = 0;
	   $londegW = 0;
	   $londegE = 0;
	   $minAbsX = 0;
	   $maxAbsX = 0;

		// First create the requested LUT
		$array = explode("\n", file_get_contents($LUTfile));
		$numlines = count($array);
		$lutSplit=" ";
		//echo 'numlines = ' . $numlines . "<br>\n";
		$vals = explode($lutSplit,$array[3]);
		//echo "Num space Lut args = " . count($vals) . "<br>\n";
		if (count($vals)<=1) // try tab instead
		{
		   $lutSplit="	";
		   $vals = explode($lutSplit,$array[3]);
		   //echo "Num tab Lut args = " . count($vals) . "<br>\n";
		}

		$lut = array();
		$ind = 0;
		$indoff=0;
		if (count($vals)>3) $indoff=count($vals)-3;

		for ($y = 3; $y < 259; ++$y) {
		  $vals = explode($lutSplit,$array[$y]);
		  $lut[$ind++] = $vals[$indoff];
		  $lut[$ind++] = $vals[$indoff+1];
		  $lut[$ind++] = $vals[$indoff+2];
		}

		// check to see whether the filename indicates it is a modis tile
		$MODISmatch = 0;
		$hpos = 0;
		$vpos = 0;
		if (fnmatch('*h??v??*',$fileName))
		{
			 // looks like a MODIS tile! So Calc min/max lat lon
			 //echo "Looks like MODIS tile<br>\n";
			 $ioff = 0;
			 $hpos = strpos($fileName,"h",$ioff);
			 while (($hpos!=null) && ($MODISmatch==0))
			 {
				$vpos = strpos($fileName,"v",$hpos);
				if ($vpos==null) $vpos = $hpos+1;
			   // echo 'hpos=' . $hpos . ' vpos=' . $vpos . "<br>\n";
				if (($vpos-$hpos)==3)
				{
					//echo "Found hXxvYY<br>\n";
					$MODISmatch = 1;
				}
				else
				{
					//echo "Found h and/or v, but not in right place<br>\n";
					$hpos = strpos($fileName,"h",$hpos+1);
				}
			 }

			 if ($MODISmatch>0)
			 {
				 //echo 'Match: hpos=' . $hpos . ' vpos=' . $vpos . "<br>\n";
				 $hh = substr($fileName,$hpos+1,2);
				 $vv = substr($fileName,$vpos+1,2);
				 $pngmaxlat = 90 - ($vv+0)*10;
				 $pngminlat = $pngmaxlat - 10;
				 //echo "XX=". $hh . " YY=" . $vv . " maxlat=" . $pngmaxlat. " MinLat=" . $pngminlat . "<br>\n";
				 $londegW = ($hh+0)*10-180;
				 $londegE = $londegW + 10;
				 $londegW = $londegW/10.0;
				 $londegE = $londegE/10.0;
			 }
		}
		/*
			 if ($MODISmatch>0)
			 {
				 $rminlat = deg2rad($pngminlat);
				 $rmaxlat = deg2rad($pngmaxlat);
				 $cosminW = $londegW/cos($rminlat);
				 $cosmaxW = $londegW/cos($rmaxlat);
				 $cosminE = $londegE/cos($rminlat);
				 $cosmaxE = $londegE/cos($rmaxlat);
				 //echo "rmin=" . $rminlat . " rmax=" . $rmaxlat . "\n";
				 //echo "lonW=" . $londegW . " cminW=" . $cosminW . " cmaxW=" . $cosmaxW . "\n";
				 //echo "lonE=" . $londegE . " cminE=" . $cosminE . " cmaxE=" . $cosmaxE . "\n";
				 $pngminlon = $cosmaxW;
				 $pngmaxlon = $cosmaxE;
			 }
		*/

		// Now map tiff to pixel values
		$tiffvals = array();
		$LEN_DATA = 2;
		$row = 0;
		$col = 0;
		$ind = 0;

		$this->getTiffFilePointer($fileName . '.tif');
		//$nx = 1024/$reduce;
		//$ny = 1024/$reduce;
		$inpx = $this->numDataCols;
		$inpy = $this->numDataRows;
		$nx = (int) $this->numDataCols/$reduce;
		$ny = (int) $this->numDataRows/$reduce;

		//$MODISmatch = 0;

		if ($MODISmatch>0)
		{
		   // nx is MAX(East_longitude West_longitude)
		   $rminlat = deg2rad($pngminlat);
		   $rmaxlat = deg2rad($pngmaxlat);
		   //$EWsize = 1.0/cos($rminlat);
		   //$EWsize2 = 1.0/cos($rmaxlat);
		   //if ($EWsize2>$EWsize) $EWsize = $EWsize2;
		   //$nx = (int) ($EWsize*$inpx/$reduce);
		   //$nx = 800;

		   $minAbsX = ($londegW/cos($rminlat))*($inpx/$reduce);
		   $minAbsX2 = ($londegW/cos($rmaxlat))*($inpx/$reduce);
		   if ($minAbsX2<$minAbsX) $minAbsX = $minAbsX2;
		   $maxAbsX = ($londegE/cos($rminlat))*($inpx/$reduce);
		   $maxAbsX2 = ($londegE/cos($rmaxlat))*($inpx/$reduce);
		   if ($maxAbsX2>$maxAbsX) $maxAbsX = $maxAbsX2;
		   $nx = (int) ($maxAbsX - $minAbsX);
		   //echo 'MODIS Match, nx=' . nx . "\n");
		}
		//$MODISmatch = 0;

		//debug_to_console("nx=" . $nx);
		//debug_to_console("ny=" . $ny);
		$dataOffset = $this->stripOffsets;
		fseek($this->fp, $dataOffset, SEEK_SET);
		$dataBytes = fread($this->fp, self::LEN_OFFSET);
		$data = unpack('VdataOffset', $dataBytes);
		$dataStart = $data['dataOffset'];
		$maxpixval = 0;

		for ($y = 0; $y < $ny; ++$y) {
		   //$dataOffset = $this->stripOffsets + (($row+$y*$reduce) * self::LEN_OFFSET);
		   //$dataOffset = $this->stripOffsets + (($y*$reduce) * self::LEN_OFFSET);

		   // $dataOffset = $this->stripOffsets + (($y*4/3) * self::LEN_OFFSET);
		   // fseek($this->fp, $dataOffset, SEEK_SET);
		   // $dataBytes = fread($this->fp, self::LEN_OFFSET);
		   // $data = unpack('VdataOffset', $dataBytes);

		   // this is the offset of the 1st column in the required data row
		   //$firstColOffset = $data['dataOffset'];
		   //$firstColOffset = $dataStart + $y * $reduce * $nx * $reduce * $LEN_DATA;
		   $firstColOffset = $dataStart + $y * $reduce  * $inpx * $LEN_DATA;
		   // now work out the required column offset relative to the 1st column
		   $requiredColOffset = 0; //$col * $LEN_DATA;

		   // combine the two and read the elevation data at that address
		   //fseek($this->fp, $firstColOffset + $requiredColOffset, SEEK_SET);
		   fseek($this->fp, $firstColOffset, SEEK_SET);
		   $numBytes = $LEN_DATA*$inpx;
		   $dataBytes = fread($this->fp, $numBytes);
		   //$fmtspec = 's' . $nx . 'pix';
		   //$data = unpack($fmtspec, $dataBytes);
		   //$data = unpack('s', $dataBytes);
		   //echo "y = " . $y . " dataBytes:" . $dataBytes[0] . ", " . $dataBytes[1] .
		   //     ", " . $dataBytes[2] . ", " . $dataBytes[3] . "<br>\n";

		   if ($MODISmatch>0)
		   {
			  $rdeglat = $pngmaxlat - $y*($pngmaxlat-$pngminlat)/$ny;
			  $rlat = deg2rad($rdeglat);
			  $coslat = cos($rlat);
			  //$minX = ($londegW/$coslat)*($inpx/$reduce) - $minAbsX;
			  $minX = ($londegW/$coslat)*($inpx/$reduce) - $minAbsX;
			  //$maxX = ($londegE/$coslat)*($inpx/$reduce) - $minAbsX;
			  $maxX = $minX + (1.0/$coslat)*($inpx/$reduce);

			  //for ($x=0; $x<$minX; $x++)
			  //   $tiffvals[$y*$nx+$x] = 241;
			  $xscale = $reduce*$coslat;

			  for ($x=$minX; $x<$maxX; $x++)
			  {
				  $ind = 2*(int)(($x-$minX)*$xscale);
				  $pixval = ord($dataBytes[$ind]) + 256*ord($dataBytes[$ind+1]);
				  if ($pixval>32767) $pixval=0;
				  $tiffvals[$y*$nx+$x] = $pixval;
				  if ($pixval>$maxpixval) $maxpixval=$pixval;
			  }
			  //for ($x=$maxX; $x<$nx; $x++)
			  //   $tiffvals[$y*$nx+$x] = 241;
		   }
		   else
		   {
			  for ($x=0; $x<$nx; $x++)
			  {
				  $ind = 2*$x*$reduce;
				  $pixval = ord($dataBytes[$ind]) + 256*ord($dataBytes[$ind+1]);
				  if ($pixval>32767) $pixval=0;
				  $tiffvals[$y*$nx+$x] = $pixval;
				  if ($pixval>$maxpixval) $maxpixval=$pixval;
				 //$tiffvals[$ind++] = (ord($dataBytes[$ind]) & 255);
			  }
		   }
		   //echo "y = " . $y . " tiffvals:" . $tiffvals[$ind-3] . ", "
		   //. $tiffvals[$ind-2] . ", ". $tiffvals[$ind-1] . ", ". "<br>\n";
		}
		//for ($y = 0; $y < count($tiffvals); ++$y) {
		//   $tiffvals[$y] =  $tiffvals[$y] & 255;
		//}
		$pixscale = $maxpixval/256;

		//$pixscale = 1;
		// Grab the dimensions of the pixel array
		//$nx = 255; //count($pixelArray, 0);
		//$ny = 255; //count($pixelArray);
		// ensure zero-value is transparent
		//$lut[0] = 0;
		//$lut[1] = 0;
		//$lut[2] = 0;
		for ($y = 0; $y < $ny; ++$y) {
			for ($x = 0; $x < $nx; ++$x) {
				//$lutind = 3*(($y + $x) & 255);
				$lutind = 3*((int)($tiffvals[$y*$nx+$x]/$pixscale) & 255);
				$pixvals[$y*$nx+$x] = $lut[$lutind] + 256*($lut[$lutind+1] + 256*$lut[$lutind+2]);
			}
		}

		// Create the image resource
		$img = imagecreatetruecolor($nx, $ny);

		// Set each pixel to its corresponding color stored in $pixelArray
		for ($y = 0; $y < $ny; ++$y) {
			for ($x = 0; $x < $nx; ++$x) {
				imagesetpixel($img, $x, $y, $pixvals[$y*$nx+$x]);
			}
		}
		$color = imagecolorallocate($img, $lut[0], $lut[1], $lut[2]);
		//$color = imagecolorallocate($img, 0,0,0);
		imagecolortransparent($img, $color);

		// output to png file
		imagepng($img, 'MapDisplay.png');
		//xx imagepng($img, $fileName . '.png');

		// Clean up after ourselves
		imagedestroy($img);
	}

public function GetPolygonForLine($pixelY,$polyMsg)
{
  $nodes=0;
  $nodePos = array();
  $polyStart = 0;
  $polyPoints = count($latarr);

  $polyMsg = $polyMsg . 'Debug: ' . $nodes . ', ' . $polyPoints . ', row=' . $pixelY . "<br>\n";

  //  Build a list of X-nodes.
  $j=$polyStart+$polyPoints-1;
  for ($i=$polyStart; $i<$polyStart+$polyPoints; $i++)
  {
	if ($polyY[$i]<$pixelY && $polyY[$j]>=$pixelY
	||  $polyY[$j]<$pixelY && $polyY[$i]>=$pixelY)
	{
	  $nodePos[$nodes++]=($polyX[$i]+($pixelY-$polyY[$i])/($polyY[$j]-$polyY[$i])
						   *($polyX[$j]-$polyX[$i]));
	}
	$j=$i;
  }

  //  Sort the nodes, via a simple “Bubble” sort.
  $i=0;
  while ($i<$nodes-1)
  {
	if ($nodePos[$i]>$nodePos[$i+1])
	{
	  $swap=$nodePos[$i]; $nodePos[$i]=$nodePos[$i+1]; $nodePos[$i+1]=$swap; if ($i>0) $i--;
	}
	else
	{
	  $i++;
	}
  }

  // Process inside polygon...
  for ($i=0; $i<$nodes; $i+=2)
  {
	if   ($nodePos[$i  ]>=$xsize) break;
	//if   (nodePos[i  ]>=nodePos[i+1]) break;

	if   ($nodePos[$i+1]> 0 )
	{
	  if ($nodePos[$i  ]< 0 ) $nodePos[$i  ]=0 ;
	  if ($nodePos[$i+1]> $xsize) $nodePos[$i+1]=$xsize;

	  for ($j=$nodePos[$i]; $j<$nodePos[$i+1]; $j++)
	  {
		 $pixval = $data[$j];
		 $polysum += $pixval;
		 $polycount++;
	  }
	}
  }
}

	/**
	* Extracts info for specified polygon.
	* Currently assumes WGS84 file
	*/
	public function getPolyVal($latlist, $lonlist, $fileName) {

		$timestamp = date("_Ymd_His");
//        $kmlFname = str_replace(".tif",$timestamp.".kml",$fileName);
//        $csvFname = str_replace(".tif",$timestamp.".csv",$fileName);
		$kmlFname = "temp.kml";
		$csvFname = "temppixels.csv";
		$meanFname = "tempmean.csv";
		$statsFname = "tempstats.csv";

		// need to convert comma-separated text strings into arrays for each of latlist and lonlist
		// finding min/max lat/lon as we go...
		$latarr = explode(',', $latlist);
		$lonarr = explode(',', $lonlist);
		$polyPoints = count($latarr);

		$minlat=min($latarr);
		$maxlat=max($latarr);
		$minlon=min($lonarr);
		$maxlon=max($lonarr);

		$kmlFile = fopen($kmlFname,"w");
		$kmlHeader='<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2">'."\n"
		."<Document><name>UserDefined</name>\n"
		."<Placemark><name>NAME1</name>\n"
		."<description>".$kmlFname."</description>\n"
		."<Polygon>\n"
		."<tessellate>1</tessellate>\n"
		."<altitudeMode>clampToGround</altitudeMode>\n"
		."<outerBoundaryIs><LinearRing><coordinates>\n";
		fwrite($kmlFile, $kmlHeader);

		for ($iNode=0;$iNode<$polyPoints;$iNode++)
		{
		   $outline = $lonarr[$iNode].",".$latarr[$iNode].",0.0\n";
		   fwrite($kmlFile, $outline);
		}
		// ensure polygon is closed...
		$outline = $lonarr[0].",".$latarr[0]."0.0\n";
		fwrite($kmlFile, $outline);

		$kmlFooter="</coordinates></LinearRing></outerBoundaryIs>\n"
		."</Polygon></Placemark></Document></kml>\n";
		fwrite($kmlFile, $kmlFooter);
		fclose($kmlFile);

		$csvFile = fopen($csvFname, "w");
		$csvinfo = 'Lat,Lon,Pixval' . "\n";
		fwrite($csvFile, $csvinfo);

		$meanFile = fopen($meanFname, "w");
		$meaninfo = 'Attribute,Area,Mean' . "\n";
		fwrite($meanFile, $meaninfo);

		$statsFile = fopen($statsFname, "w");
		$statsinfo = 'Attribute,Area,Mean,Stdev,Min,Max' . "\n";
		fwrite($statsFile, $statsinfo);

		$this->getTiffFilePointer($fileName);
		$minrow = round(($this->maxlat - $maxlat) * ($this->numDataRows -1) / ($this->maxlat - $this->minlat) );
		$maxrow = round(($this->maxlat - $minlat) * ($this->numDataRows -1) / ($this->maxlat - $this->minlat) );
		$mincol = round(($minlon - $this->minlon)* ($this->numDataCols -1) / ($this->maxlon - $this->minlon) );
		$maxcol = round(($maxlon - $this->minlon)* ($this->numDataCols -1) / ($this->maxlon - $this->minlon) );

		// Convert lat/lon coords to X,Y values for all nodes
		$polyX = array();
		$polyY = array();
		for ($iNode=0;$iNode<$polyPoints;$iNode++)
		{
		   $polyX[$iNode] = round(($lonarr[$iNode] - $this->minlon)* ($this->numDataCols -1) / ($this->maxlon - $this->minlon) ) - $mincol;
		   $polyY[$iNode] = round(($this->maxlat - $latarr[$iNode]) * ($this->numDataRows -1) / ($this->maxlat - $this->minlat) );
		}
//
		$ncols = $maxcol-$mincol+1;
		$LEN_DATA = 2*$ncols;      // ( = BitsPerSample tag value / 8)
		$dataOffset = $this->stripOffsets;
		fseek($this->fp, $dataOffset, SEEK_SET);
		$dataBytes = fread($this->fp, self::LEN_OFFSET);
		$data = unpack('VdataOffset', $dataBytes);
		$dataStart = $data['dataOffset'];

		// need to loop over minrow to max row
		$count = 0;
		$sum = 0;
		$polycount = 0;
		$polysum = 0;
		$polysumsq = 0;
		$polymin = 99999;
		$polymax = -99999;
		$debugCount = 0;
		$polyMsg = "polyMsg: ";
		//$polyMsg = 'maximgLat=' . $this->maxlat . ', maxPolyLat=' . $maxlat . ', PolyPoints=' .$polyPoints . ", polyX " . $polyX[0] . "\n";
		//$polyMsg = $polyMsg . "polyY " . $polyY[0] . "\n";
		for ($row=$minrow;$row<$maxrow;$row++)
		{
		   // get current row
		   $firstColOffset = $dataStart + ($row * $this->numDataCols + $mincol) * 2;
		   fseek($this->fp, $firstColOffset);
		   $dataBytes = fread($this->fp, $LEN_DATA);
		   $data = unpack('s'.$ncols, $dataBytes);
		   $count += ($maxcol-$mincol+1);
			// now need to extract pixels along each row which lie within the defined polygon
		   for ($col=0;$col<$ncols;$col++)
		   {
			  $sum += $data[$col];
		   }
//           if ($debugCount<5)
//           {
//              $this->GetPolygonForLine($row,$polyMsg);

// start of in-line GetPolygonForLine
  $pixelY = $row;
  $pixlat = $maxlat - $pixelY*($this->maxlat-$this->minlat)/($this->numDataRows-1);

  $nodes=0;
  $nodePos = array();
  $polyStart = 0;
  $polyPoints = count($latarr);

  //  Build a list of X-nodes.
  $j=$polyStart+$polyPoints-1;
  for ($i=$polyStart; $i<$polyStart+$polyPoints; $i++)
  {
	// $polyMsg = $polyMsg . 'Line ' . $row . '$i=' .$i . ' polyY=' . $polyY[$j] . ', ' . $polyY[$i] ."<br>\n";
	if ($polyY[$i]<$pixelY && $polyY[$j]>=$pixelY
	||  $polyY[$j]<$pixelY && $polyY[$i]>=$pixelY)
	{
	  $nodePos[$nodes++]=intval($polyX[$i]+($pixelY-$polyY[$i])/($polyY[$j]-$polyY[$i])
						   *($polyX[$j]-$polyX[$i]));
	}
	$j=$i;
  }
  //$polyMsg = $polyMsg . 'Y=' . $pixelY . ', nodes=' . $nodes . ', ' . $polyPoints . ', row=' . $pixelY . "<br>\n";
  //  Sort the nodes, via a simple “Bubble” sort.
  $i=0;
  while ($i<$nodes-1)
  {
	if ($nodePos[$i]>$nodePos[$i+1])
	{
	  $swap=$nodePos[$i]; $nodePos[$i]=$nodePos[$i+1]; $nodePos[$i+1]=$swap; if ($i>0) $i--;
	}
	else
	{
	  $i++;
	}
  }
  //$polyMsg = $polyMsg . 'Nodes: ' . $nodePos[0] . ', ' . $nodePos[1] . "<br>\n";

  // Process inside polygon...
  for ($i=0; $i<$nodes; $i+=2)
  {
	//$polyMsg = $polyMsg . '$i=' . $i . ', nodePos: ' . $nodePos[$i] . ', ' . $nodePos[$i+1] . "<br>\n";
//tbd    //if   ($nodePos[$i  ]>=$xsize) break;
	//if   (nodePos[i  ]>=nodePos[i+1]) break;

	if   ($nodePos[$i+1]> 0 )
	{
//tbd      //if ($nodePos[$i  ]< 0 ) $nodePos[$i  ]=0 ;
//tbd      //if ($nodePos[$i+1]> $xsize) $nodePos[$i+1]=$xsize;

	  for ($j=$nodePos[$i]; $j<$nodePos[$i+1]; $j++)
	  {
		 $pixval = $data[$j];
		 if ($pixval!="")
		 {
			if (($pixval<$polymin) && ($pixval>0)) $polymin = $pixval;
			if ($pixval>$polymax) $polymax = $pixval;

			$pixlon = $minlon + $j*($this->maxlon-$this->minlon)/($this->numDataCols-1);
			$csvinfo = $pixlat . ',' . $pixlon . ',' . $pixval . "\n";
			fwrite($csvFile, $csvinfo);
			$polysum += $pixval;
			$polysumsq += $pixval*$pixval;
			$polycount++;
		 }
	  }
	  //$polyMsg = $polyMsg . '$i=' . $i .   'polycount = ' . $polycount . "<br>\n";
	}
	//$polyMsg = $polyMsg . 'polycount = ' . $polycount . ', polysum= ' . $polysum  . "<br>\n";;
  }
// end of in-line GetPolygonForLine
//           }
		   $debugCount++;
		} // loop over rows
//
		//$msg = 'Lat: ' . $minlat . ', ' . $maxlat . ', Lon: ' . $minlon . ', ' . $maxlon;
		//$msg = 'Rows: ' . $minrow . ', ' . $maxrow . ', Cols: ' . $mincol . ', ' . $maxcol;
		//$mean = $sum/$count;
		$polystdev = 0;
		if ($polycount>0)
		{
			$polysum = $polysum/$polycount;
			$polystdev = sqrt( $polysumsq/$polycount - $polysum*$polysum);
		}
		if ($polymin>$polymax) $polymin=$polymax;

		//$msg = 'count=' . $count . ', mean='. intval($mean) . ', polycount=' . $polycount . ', polymean=' . intval($polysum);
		//$msg = 'Area=' . $polycount . ', Mean=' . intval($polysum) . ', Min=' . intval($polymin). ', Max=' . intval($polymax) ;
		$msg = $polycount . ',' . intval($polysum) . ',' . intval($polystdev) . ','. intval($polymin). ',' . intval($polymax) ;
		echo $msg . ";\n" ;

		fwrite($statsFile, "Attr1," . $msg . "\n");
		fwrite($meanFile, "Attr1," . $polycount . ',' . intval($polysum)."\n");

		fclose($csvFile);
		fclose($meanFile);
		fclose($statsFile);

		return $msg;
	}

	/**
	* Returns the pixel value for a given Latitude and Longitude
	* where N & E are positive and S & W are negative
	* e.g. Lat 55?30'N, Lon 002?20'W is entered as (55.5, -2.333333)
	*
	* @param float $latitude
	* @param float $longitude
	* @param string $fileName
	*/
	public function getPixVal($latitude, $longitude, $fileName) {

		$this->getTiffFilePointer($fileName);

		// check to see whether the filename indicates it is a modis tile
		$MODISmatch = 0;
		$hpos = 0;
		$vpos = 0;
		if (fnmatch('*h??v??*',$fileName))
		{
			 // looks like a MODIS tile! So Calc min/max lat lon
			 //echo "Looks like MODIS tile<br>\n";
			 $ioff = 0;
			 $hpos = strpos($fileName,"h",$ioff);
			 while (($hpos!=null) && ($MODISmatch==0))
			 {
				$vpos = strpos($fileName,"v",$hpos);
				if ($vpos==null) $vpos = $hpos+1;
			   // echo 'hpos=' . $hpos . ' vpos=' . $vpos . "<br>\n";
				if (($vpos-$hpos)==3)
				{
					//echo "Found hXxvYY<br>\n";
					$MODISmatch = 1;
				}
				else
				{
					//echo "Found h and/or v, but not in right place<br>\n";
					$hpos = strpos($fileName,"h",$hpos+1);
				}
			 }

			 if ($MODISmatch>0)
			 {
				 //echo 'Match: hpos=' . $hpos . ' vpos=' . $vpos . "<br>\n";
				 $hh = substr($fileName,$hpos+1,2);
				 $vv = substr($fileName,$vpos+1,2);

				 $pngmaxlat = 90 - ($vv+0)*10;
				 $pngminlat = $pngmaxlat - 10;
				 $londegW = ($hh+0)*10-180;
/*
				 //echo "XX=". $hh . " YY=" . $vv . " maxlat=" . $pngmaxlat. " MinLat=" . $pngminlat . "<br>\n";
				 $londegW = ($hh+0)*10-180;
				 $londegE = $londegW + 10;
				 $londegW = $londegW/10.0;
				 $londegE = $londegE/10.0;
*/
			  $ypos = ($pngmaxlat - $latitude)*$this->numDataRows/($pngmaxlat-$pngminlat);
			  $rlat = deg2rad($latitude);
			  $coslat = cos($rlat);
			  $rdx = $longitude * ($coslat - 1.0);
			  $xpos = ($longitude+$rdx-$londegW)*$this->numDataCols/10.0;
			  //$minX = ($londegW/$coslat)*$this->numDataCols;
			  //$col = (($longitude-$londegW)/$coslat)*$this->numDataCols;
			  $row = (int) $ypos;
			  $col = (int) $xpos;
			  //echo "(row=" . $row . ", col=" . $col . ") ";
			 }
		}

		if ($MODISmatch==0)
		{
		  $row = round(($this->maxlat - $latitude) * ($this->numDataRows -1) / ($this->maxlat - $this->minlat) );
		  $col = round(($longitude - $this->minlon)* ($this->numDataCols -1) / ($this->maxlon - $this->minlon) );
		}

		// get the pixel value for the calculated row & column
		$PixVal =  $this->getRowColumnData($row , $col);
//        echo 'PixVal = ' . $PixVal . "<br>\n";

		echo $PixVal . ', ';

		return $PixVal;
	}

	/**
	* Read the data file and get a pointer to the first data offset
	*
	* @param string $fileName
	*/
	private function getTiffFilePointer($fileName) {

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


		// close any previous file pointer
		if ($this->fp) {
			fclose($this->fp);
		}
		$filepath = $this->dataDir . "/". $fileName;
		if (!file_exists($filepath)){
			$this->handleError(__METHOD__ , "the file '$filepath' does not exist");
		}
		$fp = fopen($filepath, 'rb');
		if ($fp === false) {
			$this->handleError(__METHOD__ , "could not open the file '$filepath'");
		}

		// go to the file header and work out the byte order (bytes 0-1)
		// and TIFF identifier (bytes 2-3)
		fseek($fp, 0);
		$dataBytes = fread($fp, 4);
		$data = unpack('c2chars/vTIFF_ID', $dataBytes);

		// check it's a valid TIFF file by looking for the magic number
		$TIFF = $data['TIFF_ID'];
		if ($TIFF != $TIFF_ID) {
			$this->handleError(__METHOD__ , "the file '$fileName' is not a valid TIFF file");
		}

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
		else {
			self::handleError(__METHOD__ , "could not determine the byte order of the file '$fileName'");
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
					$this->numDataCols = $data['offset'];
					break;
				case $TAG_IMAGE_LENGTH :
					$this->numDataRows = $data['offset'];
					break;
				case $TAG_STRIPOFFSETS :
					$this->stripOffsets = $data['offset'];
					break;
				case $TAG_SCALE :
					$ScalePos = $data['offset'];
					break;
				case $TAG_LOCATION :
					$LocnPos = $data['offset'];
					break;
			}
		}
		$xw = $this->numDataCols;
		$yw = $this->numDataRows;
		//echo 'Xsize= ' . $xw  . "<br>\n";
		//echo 'Ysize= ' . $yw  . "<br>\n";

		fseek($fp, $ScalePos);
		$dataBytes = fread($fp, 16) ;
		$dval = unpack('d2val', $dataBytes);
		//echo 'ScaleX=' . $dval['val1'] . '  ScaleY=' . $dval['val2'] . "<br>\n";

		fseek($fp, $LocnPos);
		$dataBytes = fread($fp, 48) ;
		$locval = unpack('d6val', $dataBytes);
		$this->maxlat = $locval['val5'];
		$this->minlon = $locval['val4'];
		$this->maxlon = $locval['val4']+$xw*$dval['val1'];
		$this->minlat = $locval['val5']-$yw*$dval['val2'];
//        echo 'Xsize= ' . $xw  . ' MinLon=' . $locval['val4'] . ' MaxLon=' . $this->maxlon . "<br>\n";
//        echo 'Ysize= ' . $yw  . ' MinLat=' . $this->minlat . ' MaxLat=' . $locval['val5'] . "<br>\n";

		$this->fileName = $fileName;
		$this->fp = $fp;
	}

	/**
	* Returns the elevation data at a given zero-based row and column
	* using the current file pointer
	*
	* @param int $row
	* @param int $col
	*/
	private function getRowColumnData($row, $col) {

		$LEN_DATA = 2;             // the number of bytes containing each item of elevation data
								   // ( = BitsPerSample tag value / 8)
//        echo 'Col X = ' . $col . "<br>\n";
//        echo 'Row Y = ' . $row . "<br>\n";
		$dataOffset = $this->stripOffsets;
		fseek($this->fp, $dataOffset, SEEK_SET);
		$dataBytes = fread($this->fp, self::LEN_OFFSET);
		$data = unpack('VdataOffset', $dataBytes);
		$dataStart = $data['dataOffset'];

		// find the location of the required data row in the StripOffsets data
		//$dataOffset = $this->stripOffsets + ($row * self::LEN_OFFSET);
		//fseek($this->fp, $dataOffset);
		//$dataBytes = fread($this->fp, self::LEN_OFFSET);
		//$data = unpack('VdataOffset', $dataBytes);
		// this is the offset of the 1st column in the required data row
		//$firstColOffset = $data['dataOffset'];
		// now work out the required column offset relative to the 1st column
		//$requiredColOffset = $col * $LEN_DATA;
		$firstColOffset = $dataStart + ($row * $this->numDataCols + $col) * $LEN_DATA;
		// combine the two and read the elevation data at that address
		//fseek($this->fp, $firstColOffset + $requiredColOffset);
		fseek($this->fp, $firstColOffset);
		$dataBytes = fread($this->fp, $LEN_DATA);
		$data = unpack('spixval', $dataBytes);

		$elevation = $data['pixval'];
		return $elevation;
	}

	/**
	* Error handler
	*
	* @param string $error
	*/
	private function handleError($method, $message) {

		if ($this->showErrors) {
			ob_start();
			var_dump($this);
			$dump = ob_get_contents();
			ob_end_clean();
			die("Died: error in $method: $message <pre>$dump</pre>");
		}
		else {
			die();
		}
	}
}

?>
