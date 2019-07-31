"""cms指纹 框架指纹"""

FINGERPRINTS ={ # 这里只对请求头进行判断
    # py
    "flask": "flask",
    "wsgiserver": "Django",
    "python/": "Django",
    "csrftoken=": "Django",
    "web2py": "Web2Py - Python Framework",
    "_jcr_content": "Apache Jackrabbit/Adobe CRX repository",
    "karrigell": "Karrigell - Python Framework",
    # asp
    "x-aspnetmvc-version": "ASP.NET Framework",
    "x-aspnetmvc-version": "ASP.NET Framework",
    "x-aspnet-version": "ASP.NET Framework",
    "__requestverificationtoken": "ASP.NET Framework",
    "asp.net": "ASP.NET Framework",
    "anonymousID=": "ASP.NET Framework",
    "chkvalues=": "ASP.NET Framework",
    # php
    "CAKEPHP=": "CakePHP - PHP Framework",
    "CherryPy": "CherryPy - Python Framework",
    "ci_session=": "CodeIgniter - PHP Framework",
    "fuelcid=": "FuelPHP - PHP Framework",
    "webmail_version=": "Horde - PHP Framework",
    "webmail4prod==": "Horde - PHP Framework",
    "laravel_session=": "Larvel - PHP Framework",
    "Nette Framework": "Nette - PHP Framework",
    "Nette": "Nette - PHP Framework",
    "nette-browser=": "Nette - PHP Framework",
    "phalcon-auth": "Phalcon - PHP Framework",
    "phalconphp.com": "Phalcon - PHP Framework",
    "phalcon": "Phalcon - PHP Framework",
    # perl
    "Dancer": "Dancer - Perl Framework",
    "dancer.session=": "Dancer - Perl Framework",
    # java
    "grails": "Grails - Java Framework",
    "x-grails": "Grails - Java Framework",
    "x-grails-cached": "Grails - Java Framework",
    "play! framework;": "Play - Java Framework",
    "springframework": "Spring Framework (Java Platform)",
    # ruby
    "rails": "rails",
    "phusion passenger": "rails",
    "_rails_admin_session=": "rails",
    "x-rails": "rails",
}