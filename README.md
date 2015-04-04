www.gdg-london.com [[![Build Status](https://travis-ci.org/gdglondon/gdg-london-website.svg?branch=master)](https://travis-ci.org/gdglondon/gdg-london-website)](https://travis-ci.org/gdglondon/gdg-london-website)
==================

GDG London Website running on App Engine

### Prerequisites
This is intentionally not part of Makefile, mostly because of Travis
can't access these git repos over SSH. If we'd change it to `https://` or `git://`,
it would make it more difficult to update these dependencies in place locally.

```
git submodule init
git submodule update
```

@radeksimko: (purely personal opinion)
Git submodules suck anyway :poop:, we should replace :fire: it with
any real and proper :shower: dependency manager ([bower](http://bower.io/)?)

### How to test changes locally?

```
make serve
```

### How to deploy?

```
make deploy
```
