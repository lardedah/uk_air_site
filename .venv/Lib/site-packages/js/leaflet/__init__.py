from fanstatic import Library, Resource

library = Library('leaflet', 'resources')

leaflet_css = Resource(
    library,
    'leaflet.css',
    minified='leaflet.min.css',
    minifier='cssmin'
)

def render_ie_css(url):
    return '<!--[if lte IE 8]><link rel="stylesheet" type="text/css" href="%s" /><![endif]-->' % (url,)

leaflet_ie_css = Resource(
    library,
    'leaflet.ie.css',
    minified='leaflet.ie.min.css',
    minifier='cssmin',
    renderer=render_ie_css
)

leaflet = Resource(
    library,
    'leaflet-src.js',
    minified='leaflet.js',
    minifier=None,
    bottom=True,
    depends=(leaflet_css, leaflet_ie_css)
)
