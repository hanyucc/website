from enum import Enum
import os
from bs4 import BeautifulSoup

STYLE_ASSETS = [
  'font-awesome/css/font-awesome.css' ,
  'bootstrap.min.css',
  'style.css'
]

class FontAwesomeIcons(str, Enum):
  NONE        = ''
  PDF         = 'fa fa-file-pdf-o'
  ENVELOPE    = 'fa fa-envelope'
  ARCHIVE     = 'fa fa-archive'
  BOOK        = 'fa fa-book'
  GITHUB      = 'fa fa-github'
  ZIP         = 'fa fa-file-archive-o'
  CODE        = 'fa fa-file-code-o'
  COPY        = 'fa fa-clipboard'
  GLOBE       = 'fa fa-globe'
  BACK_ARROW  = 'fa fa-long-arrow-left'
  GRAD_CAP    = 'fa fa-graduation-cap'
  MAP_MARKER  = 'fa fa-map-marker'
  FILE        = 'fa fa-file'
  LINKEDIN    = 'fa fa-linkedin-square'

class Person:
  def __init__(self, name, website, me = False):
    self.name = name
    self.website = website
    self.me = me

class Publication:
  def __init__(self,
               image,
               title,
               authors = [],
               joint_authors = {},
               venue = '',
               resources = []):
    self.image = image
    self.title = title
    self.authors = authors
    self.joint_authors = joint_authors
    self.venue = venue
    self.resources = resources

  def get_author_suffix(self, author):
    suffix = ''
    for contribution_suffix, authors in self.joint_authors.items():
      if author in authors:
        suffix = contribution_suffix
    return suffix

  def get_author_names(self):
    names = ''
    for i, author in enumerate(self.authors):
      name = author.name
      name += self.get_author_suffix(author)

      if (author.me):
        names += f'<b>{name}</b>'

      elif (len(author.website) > 0):
        names += f'<a href={author.website}>{name}</a>'

      else:
        names += f'<a>{name}</a>'

      if i < len(self.authors) - 1:
        names += ', '
      elif i == len(self.authors) - 2:
        names += 'and'

    return names

  def get_resources(self):
    resource_list = ''
    for resource in self.resources:
      resource_list += f'''
        <div class="pr-3">
          <i class="{resource.icon}"></i>
          <a href="{resource.path}">
            {resource.name}
          </a>
        </div>
      '''
    return resource_list

class ProjectResources:
  def __init__(self, publication = [], code = []):
    self.publication = publication
    self.code = code

class Resource:
  def __init__(self, icon = FontAwesomeIcons.NONE, path = '', name = ''):
    self.icon = icon
    self.path = path
    self.name = name

class Course:
  def __init__(self, role, name, semesters = []):
    self.role = role
    self.name = name
    self.semesters = semesters

class Video:
  def __init__(self, name, id):
    self.name = name
    self.id = id

class AboutMe:
  def __init__(self, name, image, resources):
    self.name = name
    self.image = image
    self.resources = resources

  def get_html(self):
    links = ''
    for resource in self.resources:
      links += f'''
        <div class="d-block profile-row">
          <i class="{resource.icon}"></i>
          <a
            class="pl-2"
            href="{resource.path}"
          >
            {resource.name}
          </a>
        </div>
      '''
    return f'''
      <div class="d-flex pl-5 pt-5 justify-content-start">
        <div>
          <img
            id="profile-pic"
            class="float-left"
            src="{self.image}"
            title="Photo taken in front of Mt. Fuji"
            alt="Hanyu"
          />
        </div>
        <div class="col">
          <div class="d-block profile-row">
            <h1 class="name">{self.name}</h1>
          </div>
          {links}
        </div>
      </div>
    '''

class Home:
  def __init__(self, about_me, bio, publications = [], courses = []):
    self.about_me = about_me
    self.bio = bio
    self.publications = publications
    self.courses = courses

  def get_publications_list_html(self):
    pub_list = ''
    for _, pub in self.publications.items():
      pub_list += f'''
        <div>
          <div class="d-flex flex-row pb-4">
            <img
              src={pub.image}
              class="publication-thumbnail img-responsive img-thumbnail"
            />
            <div class="d-flex flex-column pl-4">
              <h5>{pub.title}</h5>
              <div>
                {pub.get_author_names()}
              </div>
              <div>
                {pub.venue}
              </div>
              <div class="d-flex flex-row justify-content-start pt-2">
                {pub.get_resources()}
              </div>
            </div>
          </div>
        </div>
      '''
    return pub_list

  def get_teaching_list_html(self):
    teaching_list = '<ul>'
    for course in self.courses:
      course_links = ''
      for i in range(len(course.semesters)):
        trailing_mark = '' if i == len(course.semesters) - 1 else ', '
        if len(course.semesters[i].path) > 0:
          course_links += f'''
            <a href="{course.semesters[i].path}">
              {course.semesters[i].name + trailing_mark}
            </a>
          '''
        else:
          course_links += f'''
            {course.semesters[i].name + trailing_mark}
          '''
      teaching_list += f'''
        <li>
          <div class="d-flex flex-row pb-4">
            <div class="d-flex flex-column pl-4">
              <div>
                {course.name}
              </div>
              <div>
                {course.role}, {course_links}
              </div>
            </div>
          </div>
        </li>
      '''

    teaching_list += '</ul>'

    return teaching_list

  def generate(self, path):
    soup = BeautifulSoup('<!DOCTYPE html> <html></html>', 'html.parser')

    # add styling
    head = soup.new_tag('head')
    soup.html.append(head)
    links = [
      soup.new_tag('link', rel='stylesheet', type='text/css',
                   href=os.path.join('assets', style_asset))
      for style_asset in STYLE_ASSETS
    ]
    [head.append(link) for link in links]

    head.append(BeautifulSoup(f'<title>{self.about_me.name}</title>', 'html.parser'))

    # construct page
    body = soup.new_tag('body')
    soup.html.append(body)
    about_me_section = self.about_me.get_html()
    publications_list = self.get_publications_list_html()
    teaching_list = self.get_teaching_list_html()
    body.append(BeautifulSoup(f'''
      <div class="container">
        {about_me_section}
      </div>
      <div class="container">
        <div class="d-flex flex-column pl-5 pt-3">
          <div>
            <p>{self.bio}</p>
          </div>
          <div class="pt-2">
            <h3>Publications</h3>
            <hr/>
            <div id="publications-list" class="pt-1">
              {publications_list}
            </div>
          </div>
          <div>
            <h3>Teaching</h3>
            <hr/>
            {teaching_list}
          </div>
          <div class="music-player-skip"></div>
          <iframe height="175" width="70%" title="Media player" src="https://embed.music.apple.com/us/album/weird-fishes-arpeggi/1109714933?i=1109715168&amp;itscg=30200&amp;itsct=music_box_player&amp;ls=1&amp;app=music&amp;mttnsubad=1109715168&amp;theme=light" id="embedPlayer" sandbox="allow-forms allow-popups allow-same-origin allow-scripts allow-top-navigation-by-user-activation" allow="autoplay *; encrypted-media *; clipboard-write" style="border: 0px; border-radius: 12px; width: 100%; height: 175px; max-width: 660px;"></iframe>
        </div>
          <div class="faux-footer"></div>
        <div class="bottom-centered">
          Design and source code based on <br><a href="https://www.bailey-miller.com/">Bailey Miller's website</a>.
        </div>
      </div>
    ''', 'html.parser'))
    with open(os.path.join(path, 'index.html'), 'w', encoding='utf-8') as file:
      file.write(str(soup))

class Project:
  def __init__(self,
               image,
               image_caption,
               abstract,
               videos = [],
               resources = ProjectResources(),
               acknowledgements= '',
               citation = ''):
    self.image = image
    self.image_caption = image_caption
    self.abstract = abstract
    self.videos = videos
    self.resources = resources
    self.acknowledgements = acknowledgements
    self.citation = citation

  def create_section(self, name, content):
    return f'''
      <div>
        <h2 class="mt-4 font-weight-normal">{name}</h2>
        <hr>
        {content}
      </div>
    '''

  def create_resources_list(self, name, resources):
    resources_list = ''
    for resource in resources:
      resources_list += f'''
        <div class="container mt-1 mb-1">
          <i class="{resource.icon}"></i>
          <a href="{resource.path}">
            {resource.name}
          </a>
        </div>
        '''
    return f'''
      <div>
        <h4 class="mt-4 font-weight-light">
          {name}
        </h4>
        {resources_list}
      </div>
    '''

  def get_abstract_html(self):
    if len(self.abstract) == 0:
      return ''
    return self.create_section('Abstract', f'<p>{self.abstract}</p>')

  def get_video_html(self):
    if len(self.videos) == 0:
      return ''
    video_list = '<div class="container">'
    for video in self.videos:
      video_list += f'''
        <div class="img-container">
        <h4 class="font-weight-light">{video.name}</h4>
          <iframe class="embed-responsive-item project-video"
                  src="https://www.youtube.com/embed/{video.id}" allowfullscreen>
          </iframe>
        </div>
      '''
    video_list += '</div>'

    return self.create_section('Videos', video_list)

  def get_resources_html(self):
    resources_html = ''

    if len(self.resources.publication) > 0:
      resources_html += self.create_resources_list('Publication', self.resources.publication)

    if len(self.resources.code) > 0:
      resources_html += self.create_resources_list('Code', self.resources.code)

    return self.create_section('Resources', resources_html)

  def get_acknowledgements_html(self):
    if len(self.acknowledgements) == 0:
      return ''
    return self.create_section('Acknowledgements', f'<p>{self.acknowledgements}</p>')

  def get_citation_html(self):
    if len(self.citation) == 0:
      return ''

    return self.create_section('Cite', f'''
      <script>
      function copyText() {{
        var text = document.getElementById("citation-to-copy")
        navigator.clipboard.writeText(text.innerText)
      }}
      </script>
      <div class="code-background">
        <button class="code-copy-btn" onClick=copyText()>
          <i class="{FontAwesomeIcons.COPY}"></i>
        </button>
        <pre id="citation-to-copy">
        {self.citation}</pre>
      </div>
      '''
    )

  def generate(self, path, publication):
    soup = BeautifulSoup('<!DOCTYPE html> <html></html>', 'html.parser')

    # add styling
    head = soup.new_tag('head')
    soup.html.append(head)
    links = [
      soup.new_tag('link', rel='stylesheet', type='text/css',
                   href=os.path.join('../../assets', style_asset))
      for style_asset in STYLE_ASSETS
    ]
    [head.append(link) for link in links]

    # construct page
    body = soup.new_tag('body')
    soup.html.append(body)
    body.append(BeautifulSoup(f'''
      <div class="container">
        <nav class="navbar navbar-expand-lg">
          <div class="container-fluid">
            <ul class="navbar-nav ml-auto">
              <li class="nav-item">
                <a href="../../">
                <i class="{FontAwesomeIcons.BACK_ARROW}"></i>
                home
                </a>
                </li>
            </ul>
          </div>
        </nav>
        <h1 class="card-title font-weight-normal">{publication.title}</h1>
        <h5 class="font-weight-light"> {publication.get_author_names()} </h5>
        <img src={project.image} class="card-img-top mt-3" alt="{publication.title}-teaser">
        <p class="font-italic mt-2">{project.image_caption} </p>
        {self.get_abstract_html()}
        {self.get_resources_html()}
        {self.get_video_html()}
        {self.get_citation_html()}
        {self.get_acknowledgements_html()}
      </div>
    ''', 'html.parser'))

    if not os.path.exists(path):
      os.makedirs(path)

    with open(os.path.join(path, 'index.html'), "w") as file:
      file.write(str(soup.prettify(formatter="html")))

PEOPLE = {
  'hanyu-chen': Person(
    name = 'Hanyu Chen',
    website = 'https://hanyuc.com',
    me = True
  ),
  'ioannis-gkioulekas': Person(
    name = 'Ioannis Gkioulekas',
    website = 'https://www.cs.cmu.edu/~igkioule/'
  ),
  'bailey-miller': Person(
    name = 'Bailey Miller',
    website = 'https://www.bailey-miller.com/'
  ),
  'alice-lai': Person(
    name = 'Alice Lai',
    website = 'https://www.linkedin.com/in/alicelai5/'
  )
}

ABOUT_ME = AboutMe(
  name = 'Hanyu Chen&nbsp;&nbsp;陈&nbsp;涵宇',
  image = 'data/images/profile.jpg',
  resources=[
    # Resource(
    #   icon=FontAwesomeIcons.MAP_MARKER,
    #   name='Carnegie-Mellon University',
    #   path='https://www.cs.cmu.edu'
    # ),
    Resource(
      icon=FontAwesomeIcons.ENVELOPE,
      name='Email',
      path='mailto:hanyuc@cs.cornell.edu'
    ),
    Resource(
      icon=FontAwesomeIcons.GITHUB,
      name='Github',
      path='https://github.com/hanyucc'
    ),
    # Resource(
    #   icon=FontAwesomeIcons.GRAD_CAP,
    #   name='Google Scholar',
    #   path='https://scholar.google.com'
    # ),
    Resource(
      icon=FontAwesomeIcons.LINKEDIN,
      name='LinkedIn',
      path='https://www.linkedin.com/in/hanyu-chen-9ba563179/'
    ),
    Resource(
      icon=FontAwesomeIcons.FILE,
      name='CV',
      path='data/documents/cv.pdf'
    )
  ]
)

BIO = '''
<p>I am first year Ph.D. student in Computer Science at <a href="https://www.cornell.edu/">Cornell University</a>. Before starting my Ph.D., I received my M.S. and B.S. 
in Computer Science from <a href="https://www.cmu.edu/">Carnegie Mellon University</a>, where I was advised by <a href="https://www.cs.cmu.edu/~igkioule/">Prof. Ioannis Gkioulekas</a>. 
My research interest lies in differentiable and neural rendering for 3D reconstruction, and more generally at the intersection of graphics and 3D vision.</p>
'''

PUBLICATIONS = {
  'pub1': Publication(
    image =  'data/images/thumbnails/fast_dipole_sums.png',
    title =  '3D Reconstruction with Fast Dipole Sums',
    authors =  [
      PEOPLE['hanyu-chen'],
      PEOPLE['bailey-miller'],
      PEOPLE['ioannis-gkioulekas']
    ],
    venue = 'ACM Trans. on Graph. (SIGGRAPH Asia), 2024',
    resources = [
      Resource(
        icon = FontAwesomeIcons.GLOBE,
        name = 'project',
        path = '#'
      ),
      Resource(
        icon = FontAwesomeIcons.PDF,
        name = 'paper',
        path = '#'
      ),
      Resource(
        icon = FontAwesomeIcons.BOOK,
        name = 'arXiv',
        path = 'https://arxiv.org/abs/2405.16788'
      )
    ]
  ),
  'pub2': Publication(
    image =  'data/images/thumbnails/volumetric_opaque_solids.png',
    title =  'Objects as Volumes: A Stochastic Geometry Theory for Opaque Solids',
    authors =  [
      PEOPLE['bailey-miller'],
      PEOPLE['hanyu-chen'],
      PEOPLE['alice-lai'],
      PEOPLE['ioannis-gkioulekas']
    ],
    venue = 'CVPR, 2024 <span style="color: #F09858;">(best student paper honorable mention)</span>',
    resources = [
      Resource(
        icon = FontAwesomeIcons.GLOBE,
        name = 'project',
        path = 'https://imaging.cs.cmu.edu/volumetric_opaque_solids'
      ),
      Resource(
        icon = FontAwesomeIcons.PDF,
        name = 'paper',
        path = 'data/papers/volumetric_opaque_solids.pdf'
      ),
      Resource(
        icon = FontAwesomeIcons.BOOK,
        name = 'arXiv',
        path = 'https://arxiv.org/abs/2312.15406'
      )
    ]
  )
}

COURSES = [
  Course(
    role = 'Teaching Assistant',
    name = 'Computer Graphics Practicum (Cornell CS 4621)',
    semesters = [
      Resource(
        name='Fall 2024',
        path='https://classes.cornell.edu/browse/roster/FA24/class/CS/4621'
      )
    ]
  ),
  Course(
    role = 'Teaching Assistant',
    name = 'Physics-based Rendering (CMU 15-468/668/868)',
    semesters = [
      Resource(
        name='Spring 2023',
        path='http://graphics.cs.cmu.edu/courses/15-468/2023_spring/'
      )
    ]
  ),
  Course(
    role = 'Grader',
    name = 'Algebraic Structures (CMU 21-373)',
    semesters = [
      Resource(
        name='Fall 2022',
        path='http://coursecatalog.web.cmu.edu/schools-colleges/melloncollegeofscience/departmentofmathematicalsciences/courses/#:~:text=21%2D373%20Algebraic%20Structures')
    ]
  )
]

PROJECT_PAGES = {
  # 'pub1': Project(
  #   image = 'https://placehold.co/800x400.png',
  #   image_caption = 'placeholder caption',
  #   abstract = 'placeholder abstract',
  #   resources = ProjectResources(
  #     publication = [
  #       Resource(
  #         icon = FontAwesomeIcons.PDF,
  #         path = '../../data/papers/pub1.pdf',
  #         name = 'Paper'
  #       ),
  #       Resource(
  #         icon = FontAwesomeIcons.BOOK,
  #         path = 'https://www.acm.org/',
  #         name =  'Publisher\'s Version'
  #       ),
  #       Resource(
  #         icon =  FontAwesomeIcons.ARCHIVE,
  #         path =  'https://arxiv.org',
  #         name =  'ArXiv Version'
  #       )
  #     ],
  #     code = [
  #       Resource(
  #         icon =  FontAwesomeIcons.GITHUB,
  #         path =  'https://github.com',
  #         name = 'Github project with full source code'
  #       )
  #     ],
  #   ),
  #   videos = [
  #     Video(
  #       name =  'presentation slides',
  #       id = 'J9o7kgrpco0'
  #     )
  #   ],
  #   acknowledgements = 'This work was generously supported by XYZ',
  #   citation = ''''''
  # )
}


if __name__ == '__main__':
  directory = 'hanyuc.com/'
  if not os.path.exists(directory):
    os.makedirs(directory)

  home = Home(about_me=ABOUT_ME,
              bio=BIO,
              publications=PUBLICATIONS,
              courses=COURSES)
  home.generate(directory)

  for id, project in PROJECT_PAGES.items():
    project_path = os.path.join(directory, f'project/{id}')
    paper = PUBLICATIONS[id]
    project.generate(project_path, paper)
