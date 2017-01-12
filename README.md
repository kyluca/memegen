# memegen.link

An API to generate meme images based solely on requested URLs.

Unix: [![Unix Build Status](http://img.shields.io/travis/jacebrowning/memegen/master.svg)](https://travis-ci.org/jacebrowning/memegen)
Windows: [![Windows Build Status](https://img.shields.io/appveyor/ci/jacebrowning/memegen.svg)](https://ci.appveyor.com/project/jacebrowning/memegen)
<br>
Metrics: [![Coverage Status](http://img.shields.io/coveralls/jacebrowning/memegen/master.svg)](https://coveralls.io/r/jacebrowning/memegen)
[![Scrutinizer Code Quality](http://img.shields.io/scrutinizer/g/jacebrowning/memegen.svg)](https://scrutinizer-ci.com/g/jacebrowning/memegen/?branch=master)
<br>
Issues: 
[![Stories in Ready](https://badge.waffle.io/jacebrowning/memegen.svg?label=ready&title=ready)](http://waffle.io/jacebrowning/memegen)

## Generating Images

Visit [http://memegen.link/api](http://memegen.link/api) to browse the API and view examples.

The URLs contain all the information necessary to generate the image. For example, http://memegen.link/buzz/memes/memes-everywhere.jpg produces:

![Sample Image](http://memegen.link/buzz/memes/memes-everywhere.jpg)

But, the site can also produce masked URLs to conceal the joke:

http://memegen.link/_YnV6egltZW1lcy9tZW1lcy1ldmVyeXdoZXJl.jpg

For any image, lose the extension to see a list of all format options:

http://memegen.link/buzz/memes/memes-everywhere

### Special Characters

In URLs, spaces can be inserted using dashes or underscores:

* dash (`-`) → space (` `)
* underscore (`_`) → space (` `)
* 2 dashes (`--`) → dash (`-`)
* 2 underscores (`__`) → underscore (`_`)

Reserved URL characters can be escaped:

* tilde + Q (`~q`) → question mark (`?`)
* tilde + P (`~p`) → percentage (`%`)
* tilde + H (`~h`) → hashtag/pound (`#`)
* tilde + S (`~s`) → slash (`/`)
* 2 single qutoes (`''`) → double quote (`"`)

For example, http://memegen.link/doge/~hspecial-characters~q/underscore__-dash--.jpg produces:

![Escaped Characters](http://memegen.link/doge/~hspecial-characters~q/underscore__-dash--.jpg)

### Alternate Styles

Some memes come in multiple forms, which can be selected via `?alt=<style>`:

![Template with Styles](memegen/static/images/template.png)

For example: [http://memegen.link/sad-biden/sad-joe-biden/doesn't-think-you'll-vote.jpg?alt=scowl](http://memegen.link/sad-biden/sad-joe-biden/doesn't-think-you'll-vote.jpg?alt=scowl)

Or, you can use your own image URL as the style. For example, http://memegen.link/custom/my-pretty/background.jpg?alt=http://www.gstatic.com/webp/gallery/1.jpg produces:

![Custom Background](http://memegen.link/custom/my-pretty/background.jpg?alt=http://www.gstatic.com/webp/gallery/1.jpg)

### Alternate Fonts

Additional fonts are available (see: http://memegen.link/api/fonts) and can be selected via `?font=<name>`.

For example, http://memegen.link/joker/pick-a-different-font/people-lose-their-minds.jpg?font=typoline-demo produces:

![Custom Font](http://memegen.link/joker/pick-a-different-font/people-lose-their-minds.jpg?font=typoline-demo)

### Custom sizes

Images can be scaled to a specific width via `?width=<int>` or a specific height via `?height=
<int>`. If both parameters are provided, the image will be padded to the exact dimensions.

For example, https://memegen.link/both/width-or-height/why-not-both~q.jpg?height=350&width=600 produces:

![Custom Size](https://memegen.link/both/width-or-height/why-not-both~q.jpg?height=350&width=600)

### Preview Images

API clients that want to show a preview of an image while the user is still typing should disable caching and analytics via `?preview=true`.

### Social Media

Add `?share=true` to optimize images sizes for sharing on social media.

## Adding Templates

To add a new template, please follow the [contributor instructions](CONTRIBUTING.md).

Thanks go to [danieldiekmeier/memegenerator](https://github.com/danieldiekmeier/memegenerator) for the inspiration!

## Sample Clients

| Type | Language | Source | Link |
| :-: | :-:| :-- | :-- |
| Slack | Python | [nicolewhite/slack-meme](https://github.com/nicolewhite/slack-meme) | --- |
| Slack | Go | [CptSpaceToaster/slackbot](https://github.com/CptSpaceToaster/slackbot) | --- |
| Slack | --- | --- | http://www.memetizer.com |
| Hain | JavaScript | [Metrakit/hain-plugin-meme](https://github.com/Metrakit/hain-plugin-meme) | --- |
| Website | Clojure | [jasich/mighty-fine-memes](https://github.com/jasich/mighty-fine-memes) | http://www.mightyfinememes.com |

Additional clients can be found by searching for [code examples on GitHub](https://github.com/search?o=desc&q=%22memegen.link%22+&ref=searchresults&s=indexed&type=Code&utf8=%E2%9C%93).
