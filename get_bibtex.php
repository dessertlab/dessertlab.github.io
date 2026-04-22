<?php
        $_GET['library']=1;
        define('BIBTEXBROWSER_BIBTEX_LINKS',false); 
        require_once('bibtexbrowser.php');

	global $db1, $db2, $db3, $db4;
        $db1 = new BibDataBase();
	$db2 = new BibDataBase();
	$db3 = new BibDataBase();
	$db4 = new BibDataBase();

        $db1->load('bib/pubs_conference.bib');
        $db2->load('bib/pubs_journal.bib');
        $db3->load('bib/pubs_editorial.bib');
        $db4->load('bib/pubs_book.bib');

	$title = isset($_GET['string']) ? $_GET['string'] : '';
	$title = '.*'.$title;

	$year = isset($_GET['year']) ? $_GET['year'] : '*';

        $query1 = array('year'=>$year, 'title'=>$title);
	$query2 = array('author'=>$title);

	$entries1 = array_merge($db1->multisearch($query1), $db1->multisearch($query2));
	$entries2 = array_merge($db2->multisearch($query1), $db2->multisearch($query2));
	$entries3 = array_merge($db3->multisearch($query1), $db3->multisearch($query2));
	$entries4 = array_merge($db4->multisearch($query1), $db4->multisearch($query2));
	$entries_res = array_merge($entries1, $entries2, $entries3, $entries4);	

        foreach($entries_res as $entry){
                $entry = htmlspecialchars($entry->getFullText(),ENT_NOQUOTES|ENT_XHTML, OUTPUT_ENCODING);
                echo $entry;
                echo "\n <br><br>";
        }


?>



