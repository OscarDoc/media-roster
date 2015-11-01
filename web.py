import webbrowser
import os
import re


# Styles and scripting for the page
main_page_head = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>My media collection</title>

    <!-- Bootstrap 3 -->
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap-theme.min.css">
    <script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
    <script src="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min.js"></script>
    <style type="text/css" media="screen">
        body {
            padding-top: 80px;
        }
        .text-align-center{text-align:center}
        #navbar{
            background: #E44424;
        }
        .navbar-brand{
            color: #91C3DC;
        }
        #navbar-title{
            color: #FFF;
        }
        #trailer .modal-dialog {
            margin-top: 200px;
            width: 640px;
            height: 480px;
        }
        .hanging-close {
            position: absolute;
            top: -12px;
            right: -12px;
            z-index: 9001;
        }
        #trailer-video {
            width: 100%;
            height: 100%;
        }
        .media-tile {
            padding-bottom: 20px;
            padding-top: 20px;
            display: inline-block;
            position: relative;
            width: 430px;
            height: 390px;
        }
        .media-info{
            text-align: left;
            position: absolute;
            top: 0;
            left: 0;
            padding-left: 20px;
            background-color: #67BCDB;
            height: 100%;
            width: 100%;
            color: #FFF;
            opacity: 0;
            transition: ease-in-out 150ms opacity;
        }
        .media-tile:hover>.media-info{
            opacity: 0.95;
            transition: ease-in-out 400ms opacity;
        }
        .scale-media {
            padding-bottom: 56.25%;
            position: relative;
        }
        .scale-media iframe {
            border: none;
            height: 100%;
            position: absolute;
            width: 100%;
            left: 0;
            top: 0;
            background-color: white;
        }
    </style>
    <script type="text/javascript" charset="utf-8">
        // Pause the video when the modal is closed
        $(document).on('click', '.hanging-close, .modal-backdrop, .modal', function (event) {
            // Remove the src so the player itself gets removed, as this is the only
            // reliable way to ensure the video stops playing in IE
            $("#trailer-video-container").empty();
        });
        // Start playing the video whenever the trailer modal is opened
        $(document).on('click', '.media-tile', function (event) {
            var trailerYouTubeId = $(this).attr('data-trailer-youtube-id')
            var sourceUrl = 'http://www.youtube.com/embed/' + trailerYouTubeId + '?autoplay=1&html5=1';
            $("#trailer-video-container").empty().append($("<iframe></iframe>", {
              'id': 'trailer-video',
              'type': 'text-html',
              'src': sourceUrl,
              'frameborder': 0
            }));
        });
    </script>
</head>
'''

# The main page layout and title bar
main_page_content = '''
  <body>
    <div class="modal" id="trailer">
      <div class="modal-dialog">
        <div class="modal-content">
          <a href="#" class="hanging-close" data-dismiss="modal" aria-hidden="true">
            <img src="img/cross.png"/>
          </a>
          <div class="scale-media" id="trailer-video-container">
          </div>
        </div>
      </div>
    </div>

    <!-- Main Page Content -->
    <div class="container">
      <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
        <div class="container-fluid">
          <div class="navbar-header">
            <a id="navbar-title" class="navbar-brand" href="#">My media collection: movies, tv shows, books...</a>
          </div>
        </div>
      </div>
    </div>
    <div class="container-fluid text-align-center">
      {media_tiles}
    </div>
  </body>
</html>
'''


# A single media entry html template
media_tile_content = '''
<div class="media-tile text-center" data-trailer-youtube-id="{media_preview}" data-toggle="modal" data-target="#trailer">
    <img src="{media_image}" width="220" height="342">
    <div class="media-info">
        <h2>{media_title}</h2>
        <p>{media_description}</p>
    </div>
</div>
'''


def create_media_tiles_content(medias):
    # The HTML content for this section of the page
    content = ''
    for media in medias:
        # Extract the youtube ID from the url
        youtube_id_match = re.search(r'(?<=v=)[^&#]+', media.preview)
        youtube_id_match = youtube_id_match or re.search(r'(?<=be/)[^&#]+', media.preview)
        preview = (youtube_id_match.group(0) if youtube_id_match else None)

        # Append the tile for the media with its content filled in
        content += media_tile_content.format(
            media_title = media.title,
            media_description = media.description,
            media_image = media.image,
            media_preview = media.preview
        )
    return content


def open_media_page(media):
    # Create or overwrite the output file
    output_file = open('index.html', 'w')

    # Replace the media tiles placeholder generated content
    rendered_content = main_page_content.format(
        media_tiles = create_media_tiles_content(media))

    # Output the file
    output_file.write(main_page_head + rendered_content)
    output_file.close()

    # open the output file in the browser (in a new tab, if possible)
    url = os.path.abspath(output_file.name)

    #TODO uncomment this for project handout
    #webbrowser.open('file://' + url, new=2)
