// <!-- {% if file_tif %}
// 	{% startphp %}
// 		{% include 'php/TifPolyVal.php' %}
// 	{% endphp %}
// {% endif %} -->



// echo "Path: ";
// echo getcwd();
// echo " ===== ";
// echo "   FILE TIF: ";
// echo {{ file_tif }};

require_once 'src/templates/php/MMGeoTIFFReader.php';


// $q = $_REQUEST["q"];
// $r = $_REQUEST["r"];
// $s = $_REQUEST["s"];
// $t = $_REQUEST["t"];

$q = {{ file_tif }};
$r = {{ cLng }};
$s = {{ cLat }};
$t = "src/templates/php/";

$fileSpec = $q;
$latlist = $r;
$lonlist = $s;
$kmlroot = $t;

if (isset($t))
{
	// extract lat/lon list from kml file instead of using passed-in list
	$kmlfname='kml/'.$kmlroot.'.kml';
	//echo $kmlfname . "\n";

	if (file_exists($kmlfname))
	{
		//echo "File exists\n";
		$xml = simplexml_load_file($kmlfname);
		$value    = (string)$xml->Document->Placemark->Polygon->outerBoundaryIs->LinearRing->coordinates;
		$values   = explode("\n", trim($value));
		$coords   = array();
		foreach($values as $value) {
			$value = trim(preg_replace('/\t+/', '', $value));
			$args     = explode(",", $value);
			array_push($coords,$args[0].",".$args[1].",".$args[2]);
		}

		$istart=0;
		$iend=sizeof($coords)-1;
		//echo 'iend='.$iend;
		$latlist = "";
		$lonlist = "";
		//echo "Declared arrays\n";
		for ($i = $istart; $i < $iend; $i++)
		{
			$lonlati = explode(',',$coords[$i]);
			$lonlist = $lonlist . $lonlati[0] . ",";
			$latlist = $latlist . $lonlati[1] . ",";
			//echo $i.','. $lonlist[$i]  . ','. $latlist[$i] . "\n";
		}
		// fix:
		//$lonlist[$iend-1] = $lonlist[0];
		//$latlist[$iend-1] = $latlist[0];
	   $lonlist = substr($lonlist,0,strlen($lonlist)-1);
	   $latlist = substr($latlist,0,strlen($latlist)-3);
	}
	else
	{
		return 'Error : Failed to open the file';
	}
}

//
$fileList = array();

//echo "fileSpec=".$fileSpec."\n";

if (strpos($fileSpec,",")>0) // path with wildcard and list of attributes
{
	$opts=explode(",",$fileSpec);
	// expand each opt to a full filename
	$root=$opts[0];
	//echo "root=".$root."<br>\n";
	//echo "sizeof opts[]=".sizeof($opts)."<br>\n";
	$wild=strpos($root,"*");
//
	for ($i=1;$i<sizeof($opts)-1;$i++)
	{
		$newfile=substr($root,0,$wild) . $opts[$i] . substr($root,$wild+1,strlen($root)-$wild);
		//echo $newfile . "<br>\n";
		$fileList[$i-1] = $newfile;
	}
//
}
else
   $fileList = glob($fileSpec);

$dataReader = new MMGeoTIFFReader("."); // directory containing tif files
//echo "fileName:" . $q . "\n<br>";
//echo "lonlist=" . $lonlist ."|\n";
//echo "latlist=" . $latlist ."|\n";

$filecount = count($fileList);

//$val = $dataReader->getPolyVal($latlist, $lonlist, $fileName);
foreach ($fileList as $fileName) {
	$val = $dataReader->getPolyVal($latlist, $lonlist, $fileName);
}
//
