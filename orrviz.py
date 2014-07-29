#!/usr/bin/env python

import cgi
import cgitb

# enable tracebacks of exceptions
cgitb.enable()

from SPARQLWrapper import SPARQLWrapper, JSON
sparql = SPARQLWrapper("http://mmisw.org/sparql")
sparql.setReturnFormat(JSON)
#
#

def do_query(queryString):
    sparql.setQuery(queryString)
    j = sparql.query().convert()
    return j
   
def make_options_tags(results, varname, mark_selected=''):
    # <option VALUE="http://mmisw.org/ont/ioos/category/atmospheric" selected  > http://mmisw.org/ont/ioos/category/atmospheric
    # <option VALUE="http://mmisw.org/ont/ioos/category/chemical" > http://mmisw.org/ont/ioos/category/chemical
    # <option VALUE="http://mmisw.org/ont/ioos/category/coordinate" > http://mmisw.org/ont/ioos/category/coordinate
    options_str = ''
    for r in results["results"]["bindings"]:
        value = r[varname]['value']
        if value == mark_selected:
            options_str = options_str + '<option VALUE="%s" selected > %s ' % (value, value)
        else:
            options_str = options_str + '<option VALUE="%s" > %s ' % (value, value)
    return options_str    

def get_category_list(cat,param):
    if param=='':
        # find categories related to all parameters
        p = '?p'
    else:
        # find categories related to specific parameter
        p = '<%s>' % param  
    queryString = """
    PREFIX ioos: <http://mmisw.org/ont/ioos/parameter/>
    SELECT DISTINCT ?cat
    WHERE {%s a ioos:Parameter .
           ?cat skos:narrowMatch %s .
          } 
    ORDER BY ?cat
    """ % (p, p)
    results = do_query(queryString)
    return make_options_tags(results, 'cat', cat)

def get_parameter_list(cat,param):
    queryString = """
    PREFIX ioos: <http://mmisw.org/ont/ioos/parameter/>
    SELECT DISTINCT ?p
    WHERE {
           <%s> skos:narrowMatch ?p .
          } 
    ORDER BY ?p
    """ % (cat,)
    results = do_query(queryString)
    return make_options_tags(results, 'p', param)

def get_mapping_list(param, match):
    queryString = """
    PREFIX ioos: <http://mmisw.org/ont/ioos/parameter/>
    SELECT DISTINCT ?value
    WHERE {
           <%s> ?property ?value .
           FILTER  (regex(str(?property), "%s", "i"))
          } 
    ORDER BY ?value
    """ % (param, match)
    results = do_query(queryString)
    return make_options_tags(results, 'value', match)

def printHTTPheader():
    # print an HTTP header
    print "Content-type: text/html"
    print ""
    print ""

def main():

    form = cgi.FieldStorage()
    selected_cat = form.getvalue("catterm", 'http://mmisw.org/ont/ioos/category/atmospheric')
    selected_param = form.getvalue("paramterm", '')
    selected_match = form.getvalue("skosmatch", 'Match')

    # for debugging create an HTML list
    # of all the fields on the calling form and their values
    field_list = '<ul>\n'
    for field in form.keys():
        field_list = field_list + '<li>field: %s, value: %s</li>\n' % (field, form.getvalue(field))
    field_list = field_list + '</ul>\n'

    # create category, parameter, and mapping <select> options
    page_dict = {
        'selected_param' : selected_param, 
        'cat_option_str' : get_category_list(selected_cat, selected_param),
        'param_option_str' : get_parameter_list(selected_cat, selected_param),
        'map_option_str': get_mapping_list(selected_param, selected_match),
        'field_list' : field_list,
        }
    # manually built list
    # page_dict = {'cat_option_str' : get_category_list(),
    #              'param_option_str' : temp_parameter_list(),
    #              'map_option_str': temp_mapping_list(),
    #              }

    printHTTPheader()
    # this string contains the web page that will be served
    # test_str="""
    # %(cat_option_str)s
    # %(param_option_str)s
    # %(map_option_str)s
    # """ % page_dict
    
    page_str="""
    <html> <head>
    <title>ORR Visualizer</title>
    </head>
    
    <body onload="document.getElementById('orrbox').src='%(selected_param)s'">
    <h1>MMI-ORR IOOS Parameter Visualizer</h1>
        
    <table>
    <tr><td>

    <table>
    <form id="cat_form" method="post" action="orrviz.py">
    <tr><th colspan=2 align=right>&lt-- MORE GENERAL<br>Categories, Parents <br></th></tr>
    <tr><td colspan=2>
    <select id="catterm" name="catterm" size=10 onclick="document.getElementById('orrbox').src=this.options[this.selectedIndex].value">
    %(cat_option_str)s
    </select>
    </td></tr>
    <tr>
    <td align=left><input type="submit" value="RESET" onclick="document.getElementById('paramterm').options.selectedIndex=-1">
    <td align=right><input type="submit" value="Submit&gt&gt"></td></tr>
    </table>

    </td>
    <td >

    <table>
    <tr><th><br>Parameter Term
    </th></tr>
    <tr><td>
    <select id="paramterm" name="paramterm" size=10 onclick="document.getElementById('orrbox').src=this.options[this.selectedIndex].value">
    %(param_option_str)s
    </select>
    </td></tr>
    <tr><td align=right>
    <select id="skosmatch" name="skosmatch" size=1>
    <option value='Match' selected > Any Match
    <option value='exactMatch'> (=) exactMatch
    <option value='closeMatch'> (~) closeMatch
    <option value='narrowMatch'> (&gt) narrowMatch
    </select>
    <input type="submit" value="Submit&gt&gt"></td></tr>
    </form>
    </table>

    </td>
    <td valign=top>
    
    <table>
    <tr><th align=left>MORE SPECIFIC --&gt<br>Mappings, Similar Terms <br></th></tr>
    <td>
    <select id="mapterm" name="mapterm" size=10 onclick="document.getElementById('orrbox').src=this.options[this.selectedIndex].value">
    %(map_option_str)s
    </select>
    </td>
    </tr>	
    </table>
    
    <tr>
    <td colspan=3>
    </br>
    <iframe width="700" height="500" src="" id="orrbox" name="orrbox"></iframe>
    </td>
    </tr>

    </table>

    %(field_list)s

    </body> </html>
    """ % page_dict

     # serve the page with the data table embedded in it
    print page_str

if __name__=="__main__":
    main()
