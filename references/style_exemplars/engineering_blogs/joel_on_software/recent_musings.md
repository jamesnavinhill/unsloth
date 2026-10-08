# Joel Spolsky Recent Essays & Musings

**Source**: [https://www.joelonsoftware.com/author/joelonsoftware/](https://www.joelonsoftware.com/author/joelonsoftware/)  
**Style Profile**: Relaxed elder statesman engineering humor, candid perspective on software and business

---

* [News](https://www.joelonsoftware.com/category/news/)

Since the 1990s, the web has been a publishing place for human-readable documents. 

Documents published on the web are in HTML. HTML has a little bit of structure, for example, “here is a paragraph” or “emphasize this word.” 

Then you stir in some CSS, which adds some pretty decorations to the structure, saying things like: make those paragraphs have tiny gray sans-serif text! And then people think you are hip. Unless they are older, and they can’t read your tiny gray words, so they give up on you.

That’s “structure,” as far as it goes, on the web.

Imagine, for example, that you mention a book on the web.

**Goodnight Moon**  
by _Margaret Wise Brown_  
Illustrated by _Clement Hurd_  
Harper & Brothers, 1947  
ISBN 0-06-443017-0

There’s not much structure there. A naive computer program reading this web page might not realize I was even mentioning a book. All I did was make the title bold.

So, also since the 1990s, people have realized that we can make the web a much more useful place to publish information if we applied a bit more structure. As early as 1999, Tim Berners-Lee was writing about the [Semantic Web](https://en.wikipedia.org/wiki/Semantic_Web):

> “I have a dream for the Web [in which computers] become capable of analyzing all the data on the Web – the content, links, and transactions between people and computers. A ‘Semantic Web’, which makes this possible, has yet to emerge, but when it does, the day-to-day mechanisms of trade, bureaucracy and our daily lives will be handled by machines talking to machines. The [‘intelligent agents’](https://en.wikipedia.org/wiki/Intelligent_agent) people have touted for ages will finally materialize.”
> 
> Tim Berners-Lee, Weaving The Web, 1999 HarperSanFrancisco (Chapter 12)

Using the Semantic Web you might publish a book title with a lot more detail that makes it computer-readable. To do this, you would probably start by going to schema.org and looking up [their idea of a book](https://schema.org/Book). Then you could use one of a number of formats, like RDF or JSON-LD, to add additional markup to your HTML saying “hey! here’s a book!”

Ok, well, doing that is kinda hard to figure out, and, to be honest, it’s homework. Once your beautiful blog post is published and human-readable, it’s hard to gather the mental energy to figure out how to add the additional fancy markups that will make your web page computer-readable, and, unless there is already a computer reading your web pages, at this point, you usually give up. So, yeah. That was 1999, and not much progress has been made and there is very little of this semantic markup in the wild.

**Well.**

We would like to fix this, because human progress depends on getting more and more information in formats that are readily accessible, both by regular humans, their dumb A.I. li’l sibs, and your more traditional computer programs.

Here is something I believe: **people will only add semantic markup to their web pages if doing so is easier than not.**

In other words, the cost of adding semantic markup has to be zero or negative, or this whole project is not going anywhere.

Now imagine this world for a second:

  * I want to insert a book into my blog post
  * I type **/book**
  * A search box appears where I start typing in the title of my book and choose from an autocomplete list.
  * Once I find the book, a block gets inserted in my blog post showing details of the book in a format I like, _with nice semantic markup behind the scenes_.

In this world I did _less_ work to insert a book (because I was assisted by a UI that looked up the details for me).

You can imagine the same scenario applying to literally any other kind of structured data.

  * I want to insert an address into my blog post
  * I type **/address**
  * A search box appears where I start to type a location, which autocompletes in the way you have seen Instagram and Google Maps and a million other apps do it
  * Once I choose the address, a block gets inserted showing the details of the address complete with semantic markup behind the scenes.

My “address block” might have any visual appearance. Visitors to my web page might see the address, or a little map, or a little map in Japanese, etc. etc. The semantic content is there behind the scenes. So, for example, my web browser might know “gosh this is an address! Maybe you want to do _address-y_ things with it, like _go there_ ,” and then my browser might offer me options to summon a self-driving car and even call an ambulance when the self-driving car self-drives into a snowbank.

My two simplistic examples of “book” and “address” are interesting right now because (a) you can probably think of 1,000,000 more data types like this, and (b) none of these things work right now, because even though almost every web editing environment has a concept of “blocks,” none of them are extensible. WordPress has (oh gosh) hundreds of block types, but they don’t have thousands or millions, they don’t have “book” or “address” or “Burning Man Theme Camp” yet, and there’s no ecosystem by which developers and users can contribute _new_ block types.

So I guess I gotta wait around for someone at WordPress to develop all the blocks I want to use. And then someone at Notion, and then someone at Trello, and then someone at Mailchimp, and someone at every other vendor that provides a text editor.

## I have a better plan.

The web was built with open protocols. Suppose we all agree on a _protocol_ for blocks.

Any developer that wants to create a new block can conform to this protocol.

Any kind of web-text-editing application can also conform to this protocol.

Then if _anyone_ goes to the trouble of creating a cool “book” or “address” block, we’ll all be able to use it, anywhere.

And we shall dub this protocol, oh I don’t know, [the Block Protocol](https://blockprotocol.org/).

And it should be, I think, 100% free, open, and public, so that there is no impediment to anyone on earth using it. And in fact if you want to make blocks that are open source or public, good for you, but if for some reason you would like to make private or commercial blocks, that’s fine too.

## Where we’re up to

It’s been about a year since we started talking about the Block Protocol, and we’ve made a lot of progress figuring out how it has to work to do all the things it will need to do, in a clean and straightforward way. 

But this is all going nowhere if it requires 93,000,000 humans to cooperate with my crazy scheme just to get it off the ground.

So what we did is build a [WordPress Plugin](https://blockprotocol.org/wordpress) that allows you to embed Block Protocol blocks into posts on your WordPress sites just as easily as you insert any other block.

Since WordPress powers [43%](https://wordpress.org/about/features/) of the web, that means if you build a block for the Block Protocol, it’ll be widely usable right away.

Here’s a video demo:

The WordPress Plugin will be free, and it will be widely available in February, when we’ll also publish version 0.3 of the Block Protocol specification. You can get [early access](https://blockprotocol.org/wordpress) now.

In fact, if you were thinking of writing a plugin for WordPress for your own kind of custom block, you’ll find that using _our_ plugin as your starting point is a lot easier, because you don’t have to know anything about WordPress Plugins or write any PHP code. So even if you don’t care for any of my crazy theories and just want to add a block to WordPress, this is the way to go.

Ultimately, though, we just want to make it easier to add useful semantic, structured information to the web, and this is the first step.

PS We just set up [a Discord server for the Block Protocol](http://blockprotocol.org/discord) where you can participate, ask questions, and meet the team.

PPS You can follow me on Mastodon, where I am [@spolsky@blackrock.city](https://blackrock.city/@spolsky). I don’t post that much, but I’m enjoying hanging out there in a human-to-human environment where there isn’t an algorithm stirring up righteous indignation about the latest fake-outrage of the day.

  * [News](https://www.joelonsoftware.com/category/news/)

You’ve probably seen web editors based on the idea of _blocks_. I’m typing this in WordPress, which has a little + button that brings up a long list of potential blocks that you can insert into this page:

This kind of “insert block” user interface concept is showing up in almost every blogging tool, web editor, note-taking app, and content management system. People like it and it makes sense. 

We have seem to have standardized on one thing: the **/** key to insert a new block. Everything else, though, is completely proprietary and non-standard. 

I thought, wouldn’t it be cool if blocks were interchangeable and reusable across the web?

Until now, every app that wants blocks has to implement them from scratch. Want a calendar block? Some kind of fancy Kanban board? Something to embed image galleries? Code it up yourself, buddy.

As a result of the non-standardization of blocks, our end-users suffer. If someone is using my blog engine, they can only use those blocks that I had time to implement. Those blocks may be pretty basic or incomplete. Users might want to use a fancier block that they saw in WordPress or Medium or Notion, but my editor doesn’t have it. Blocks can’t be shared or moved around very easily, and our users are limited to the features and capabilities that we had time to re-implement.

To fix this, we’re going to create a protocol called the [Block Protocol](https://blockprotocol.org). 

It’s open, free, non-proprietary, we want it to be everywhere on the web. 

It’s just a protocol that embedding applications can use to embed blocks. Any block can be used in any embedding application if they all follow the protocol.

Our hope is that this will make life much easier for app developers to support a huge variety of block types. At the same time, anyone can develop a block once and have it work in any blog platform, note-taking app, or content management system. It is all 100% free, open, and any sample code we develop showing how to use the protocol will be open-source.

We’ve released a very early draft of the Block Protocol, and we’ve started building some very simple blocks and a simple editor that can host them.

We’re hoping to foster an open source community that creates a huge open source library of amazing blocks:

What can be a block? 

  * Anything that makes sense in a document: a paragraph, list, table, diagram, or a kanban board. 
  * Anything that makes sense on the web: an order form, a calendar, a video.
  * Anything that lets you interact with structured or typed data: I’ll get to that in a minute.

If you work on any kind of editor—be it a blogging tool, a note-taking app, a content management system, or anything like that—you should allow your users to embed blocks that conform to the Block Protocol. This way you can write the embedding code once and immediately make your editor able to embed a rich variety of block types with no extra work on your part.

If you work on any kind of custom data type that might make sense to embed in web pages, you should support the Block Protocol. That way anybody with a hosting application that supports the protocol can embed your custom data type.

Because it’s all 100% open, we hope that the Block Protocol will become a web standard and commonly used across the Internet.

That will mean that common block types, from paragraphs and lists to images and videos, will get better and better. But it will also mean that some esoteric block types will be embeddable anywhere. Want to create a block that shows the Great Circle routing for a flight between two airports? Write the code for the block once and it can be embedded anywhere. 

Oh, and **one more thing**. Blocks can be highly structured, that is, they can have types. That means that they magically become machine-readable without screen scraping. For example, if you want to create an event block to represent an event on a calendar, you will be able to specify a _schema_ that describes the event data type in a standard way. That way tools like calendars can instantly parse and understand web pages that contain your event block, reliably.

Over time, it will mean that anyone can easy publish complex, typed data sets on the web that are automatically machine-readable without extra work. (Have you ever seen one of those websites where there’s a link to “download the data set in .XLS format”? Yeah, say goodbye to that.)

**We’re going public with this very early in the development process** because we need a lot of help! 

Everything we have so far is version 0.1. It’s simple and not very good yet and going to need some iteration before it has the hope of truly being a useful web protocol. 

This is an open protocol, free and non-proprietary, and it’s going to make the open web much better if widely adopted, so we need to start getting people involved early, giving us feedback, and building new things!

[Go read more about the Block Protocol now!](https://blockprotocol.org)

  * [News](https://www.joelonsoftware.com/category/news/)

The other day I was talking to a young developer working on a code base with tons of COM code, and I told him that even before he was born, everyone knew that COM was already so deeply obsolete that it was impossible to find anyone who knew enough to work on it. And yet they still have this old COM code base, and they still have one old programmer holding onto their job by being the only human left on the planet with a brain big enough to manually manage multithreaded objects. I remember that COM was like Gödels Theorem: it seemed important, and you could understand it all long enough to pass an exam, but ultimately it is mostly just a demonstration of how far human intelligence can be made to stretch under extreme duress.

And, _bubbeleh_ , if there is one thing we have learned, it’s that the things that make it _easier_ on your brain are the things that matter.

Programming changes slowly. Really slowly.

Since I learned to code forty years ago, one thing that has mostly, _mostly_ , changed about programming is that most developers no longer have to manage their own memory. Even getting that going took a long long time.

I took a few stupid years trying to be the CEO of a growing company during which I didn’t have time to code, and when I came back to web programming, after a break of about 10 years, I found Node, React, and other goodies, which are, don’t get me wrong, amazing? Really really great? But I also found that it took approximately the same amount of work to make a CRUD web app as it always has, and that there were some things (like handing a file upload, or centering) that were, shockingly, still just as randomly difficult as they were in VBScript twenty years ago. 

Where are the flying cars?

The biggest problem is that developers of programming tools love to add things and hate to take things away. So things get harder and harder and more and more complex because there are more and more ways to do the same thing, each has pros and cons, and you are likely to spend as much time just figuring out which “rich text editor” to use as you are to implement it.

(Bill Gates, 1990: “How many f*cking programmers in this company are working on rich text editors?!”)

So, in this world of slow, gradual change and alleged improvement, one thing did change literally overnight, or, to be precise, on September 15, 2008, which was when [Stack Overflow launched](https://www.joelonsoftware.com/2008/09/15/stack-overflow-launches/).

Six-to-eight weeks before that, Stack Overflow was only an idea. (*Actually Jeff started development in April). Six-to-eight weeks after that, it was a standard part of every developer’s toolkit: something they used every day. Something _had_ changed about programming, and changed very fast: the way developers learned and got help and taught each other.

For many years, I was able to coast by telling delightful little stories about our incredible growth numbers, about the pay web site we made obsolete, and even about that one time when a Major Computer Book Publisher threatened to BURY US and launched their own Q&A platform, which turned out to be more of a Scoff Generator than a Q&A platform, but actually now almost anyone I talk to is too young to imagine The Days Before Stack Overflow, when the bookstore had an entire _wall_ of Java and the way you picked a Rich Text Editor was going to Barnes and Noble and browsing through printed books for an hour, in the Rich Text Editor Component shelf.

Stack Overflow got to be pretty big as a business. The company grew faster than any individual’s skills at managing companies, especially mine, so a lot of the business team has changed over, and we now have a really world-class, experienced team that is doing much better than us founders. We’ve done incredible work building a recruiting platform for great developers, a “reach and relevance” platform for getting developers excited about your products, and, most importantly, [Stack Overflow for Teams](https://stackoverflow.com/teams), which is growing so quickly that soon every developer in the world will be using the power of Stack Overflow to get help with their own code base, not just common languages and libraries. 

And yeah, the one thing I made sure of was that everyone that came into the company understood exactly why Stack Overflow works, and what is important to the developers that it is by and for. So while we haven’t always been perfect, we have kept true to our mission, and the current leadership is just as committed to the vision of Stack Overflow as the founders are.

Today we’re pleased to announce that Stack Overflow is joining [Prosus](https://www.prosus.com). Prosus is an investment and holding company, which means that the most important part of this announcement is that Stack Overflow will continue to operate independently, with the exact same team in place that has been operating it, according to the exact same plan and the exact same business practices. Don’t expect to see major changes or awkward “synergies”. The business of Stack Overflow will continue to focus on Reach and Relevance, and Stack Overflow for Teams. The entire company is staying in place: we just have different owners now.

This is, in some ways, the best possible outcome. Stack Overflow stays independent. The company has plenty of cash on hand to expand and deliver more features and fix the old broken ones. Right now, the biggest gating factor to how fast we can do this is just how fast we can [hire excellent people](https://stackoverflow.com/company/work-here). 

I’ve been out of the day-to-day for a while now. Together with Dei Vilkinsons, I’m helping to build [HASH](https://hash.ai). HASH makes it easy to build powerful simulations and make better decisions. As we worked on that, we discovered that too much of the data that you might need to run simulations needs to be fixed up before you can use it. That’s because data is often published on the web, using page description languages that are more concerned with formatting and consumption by humans. They lack the structure to make the data they contain readily accessed programatically, so step one is miserable screen scraping and data cleanup. That’s where a lot of people give up.

We think we have an interesting way to fix this. If it works, we’ll change the web as quickly and completely as Stack Overflow changed programming. But it’s kind of ambitious and maybe a little too GRAND. If you are interested in joining that crazy journey, do reach out. The whole thing is going to be open source, so just hang on, and we’ll have something up on GitHub for you to play with.

See you soon!

  * [News](https://www.joelonsoftware.com/category/news/)

Sometimes when you’re trying to figure out the way the world works, basic math is enough to get you going. If we increase the hot water flow by _x_ , the temperature of the mixture goes up by _y_. 

Sometimes you’re working on something that’s just too complicated for that, and you can’t even begin to guess how the inputs affect the outputs. At the warehouse, everything seems to go fine when you have less than four employees, but when you hit five employees, they get in each others’ way so much that the fifth employee effectively does no additional work.

You may not understand the relationship between the number of employees and the throughput of the warehouse, but you definitely know what everybody is doing. If you can imagine writing a little bit of JavaScript code to simulate the behavior of each of your workers, you can run a simulation and see what actually happens. You can tweak the parameters and the rules the employees follow to see how it would help, and you can really gain some traction understanding, and then solving, very complex problems.

That’s what [hash.ai](https://hash.ai/) is all about. Read Dei’s [launch blog post](https://hash.ai/about/mission), then try building your own simulations!

  * [News](https://www.joelonsoftware.com/category/news/)

For the last couple of months, Prashanth Chandrasekar has been getting settled in as the [new CEO of Stack Overflow](https://www.joelonsoftware.com/2019/09/24/announcing-stack-overflows-new-ceo/). I’m still going on some customer calls and have a weekly meeting with him, but I have freed up a lot of time. I’m also really enjoying discovering just how little I knew about running medium-sized companies, as I watch Prashanth rearrange everything—for the better. It’s really satisfying to realize that the best possible outcome for me is if he proves what a bad CEO I was by doing a much better job running the company.

Even though I live in Manhattan’s premier NORC (“Naturally Occurring Retirement Community,”) I’m thinking of this time as a [sabbatical](https://www.joelonsoftware.com/2000/03/18/more-on-sabbaticals/), not retirement. And in fact I’m really, really busy, and, in the interest of deflecting a million questions about what I’m doing nowadays, thought I’d update my long-suffering readers here.

This adorable little fella, Cooper, is two. If your web app needs a mascot, apply within. 

I’m chairman of three companies. You probably know all about Stack Overflow so I’ll skip ahead. 

Fog Creek Software has been renamed [Glitch](https://glitch.com/), “the friendly community for building the web.” Under CEO [Anil Dash](http://anildash.com/), they have grown to [millions of apps](https://www.theverge.com/2019/7/9/20683018/glitch-2-5-million-apps-code-remix-anil-dash) and raised a decent [round of money](https://glitch.com/culture/glitch-raises-30m-series-a-round-from-tiger-global/) to accelerate that growth. I think that in every era there has to be some kind of simplified programming environment for the quiet majority of developers who don’t need fancy administration features for their code, like git branches or multistep deployment processes; they just want to write code and have it run. Glitch is aimed at those developers.

The third company, [HASH](https://hash.ai/), is still kind of under the radar right now, although today they put a whole bunch of words up on their website so I guess I can give you a preview. HASH is building an open source platform for doing simulations. It’s a great way to model problems where you have some idea of how every agent is supposed to behave, but you don’t really know what all that is going to add up to.

For example, suppose you’re a city planner and you want to model traffic so that you can make a case for a new bus line. You can, sort of, pretend that every bus takes 50 cars off the road, but that’s not going to work unless you can find 50 commuters who will all decide to take your new bus line… and the way they decide is that they check if the bus is actually going to save them time and money over just driving. This is a case where you can actually simulate the behavior of every “agent” in your model, like [Cities: Skylines](https://en.wikipedia.org/wiki/City-building_game) does, and figure out the results. Then you can try thousands or millions of different potential bus routes and see which ones actually reduce traffic. 

This kind of modeling is incredibly computationally intensive, but it works even when you don’t have a closed-form formula for how bus lines impact traffic, or, in general, how individual agents’ behavior affects overall outcomes. This kind of tool will be incredibly useful in far-ranging problems, like epidemiology, econometrics, urban planning, finance, political science, and a lot of other areas which are not really amenable to closed-form modeling or common “AI” techniques. (I love putting AI in “scare” “quotes”. There are a lot of startups out there trying to train machine learning models with way too little data. Sometimes the models they create just reproduce the bad decision making of the humans they are trained on. In many cases a model with simulated agents running a white box algorithm is going to be superior). 

Ok, so those are the three companies I’m still working on in some way or another. That still leaves me with a couple of free days every week which I’m actually using to work on some electronics projects. 

In particular, I’m really into pixel-addressable RGB LEDs, like those WS2812b and APA102-type things. Right now I’m [working](https://blinkylights.blog/) on designing a circuit board that connects a Teensy 3.2 controller, which can drive up to 4416 LEDs at a high frame rate, to a WizNET Ethernet adapter, and then creating some software which can be used to distribute 4416 pixels worth of data to each Teensy over a TCP-IP network in hopes of creating huge installations with hundreds of thousands of pixels. If that made any sense at all, you’re probably already a member of the [LEDs ARE AWESOME](https://www.facebook.com/groups/LEDSAREAWESOME/) Facebook group and you probably think I’m dumb. If that doesn’t make any sense, rest assured that I am probably not going to burn down the apartment because I am very careful with the soldering iron almost every time. 

  * [News](https://www.joelonsoftware.com/category/news/)

Last March, I [shared](https://www.joelonsoftware.com/2019/03/28/the-next-ceo-of-stack-overflow/) that we were starting to look for a new CEO for Stack Overflow. We were looking for that rare combination of someone who could foster the community while accelerating the growth of our businesses, especially Teams, where we are starting to close many huge deals and becoming a hyper-growth enterprise software company very quickly. This is not something I’m particularly good at, and I thought it was time to bring on more experienced leadership.

The Board of Directors nominated a search committee and we went through almost 200 candidates. It speaks to how well respected a company Stack Overflow is that we found ourselves in the rare position of having plenty of highly qualified executives who were excited about the opportunity. Nevertheless, one of them really stood out, and we are pleased to let you know that we have selected Prashanth Chandrasekar as our next CEO. His first day will be October 1st.

Prashanth was born in Bangalore, India, the city with the highest number of Stack Overflow users in the world, one of the global capitals for software developers writing the script for the future. He started out as a software engineer before moving over to management. He has a BS in Computer Engineering from the University of Maine, a Masters in Engineering Management from Cornell, and an MBA from Harvard. He worked at Capgemini as a management consultant and Barclays as an investment banker in their technology group before joining Rackspace in San Antonio, Texas.

At Rackspace, Prashanth really proved his mettle, creating from scratch a completely new business unit inside the company, the [Global Managed Public Clouds Business](https://www.rackspace.com/cloud/public). This group serves companies around the world who need help running on AWS, Azure, Google, and so on. Under his leadership, Rackspace successfully pivoted from a leading managed hosting company to a cloud services company. And he did this while working with developers both inside Rackspace and outside, so he understands our vision of “writing the script for the future” better than anyone I’ve met.

This is an exciting time for Stack Overflow, and we have some big goals for the year ahead. We want to make Stack Overflow more diverse, inclusive, and welcoming. And we want to make it possible for knowledge workers everywhere to use Stack Overflow to get answers to the proprietary questions that are specific to their organizations and teams. We’re doing great work and making great progress in these areas, and I’m confident that Prashanth has some great ideas about how to move forward faster on all our goals.

As you know, I’m keeping my job as Chairman of the Board, so I’ll continue to be closely involved. Being Stack Overflow’s CEO has been an honor, and I can’t wait to see the things the team accomplishes in the year ahead. This will be a great new chapter for Stack Overflow.  

  * [Stack Overflow](https://www.joelonsoftware.com/category/reading-lists/stack-overflow/), [News](https://www.joelonsoftware.com/category/news/)

Big news! We’re looking for a new CEO for Stack Overflow. I’m stepping out of the day-to-day and up to the role of Chairman of the Board.

Stack Overflow has been around for more than a decade. As I look back, it’s really amazing how far it has come. 

Only six months after we had launched Stack Overflow, my co-founder Jeff Atwood and I were invited to speak at a Microsoft conference for developers in Las Vegas. We were there, I think, to demonstrate that you could use their latest ASP.NET MVC technology on a real website without too much of a disaster. (In fact .NET has been a huge, unmitigated success for us, but you kids go ahead and have fun with whatever platform you want mkay? They’re all great, or, at least, above-average).

It was a giant conference, held at the Venetian Hotel. This hotel was so big that other _hotels_ stay there when they go on vacation. The main ballroom was the size of, approximately, Ireland. I later learned there were 5,000 developers in that room.

I thought it would be a fun thing to ask the developers in the room how many of them had visited Stack Overflow. As I remember, Jeff was very much against this idea. “Joel,” he said, “That is going to be embarrassing and humiliating. Nobody is going to raise their hand.”

Well, I asked it anyway. And we were both surprised to see about one-third of the hands go up. We were really making an impact! That felt really good.

Anyway, I tried that trick again whenever I spoke to a large audience. It doesn’t work anymore. Today, audiences just laugh. It’s like asking, “Does anyone use gravity? Raise your hand if you use gravity.”

Where are we at after 11 years? Practically every developer in the world uses Stack Overflow. Including the Stack Exchange network of 174 sites, we have over 100 million monthly visitors. Every month, over 125,000 wonderful people write answers. According to Alexa, [stackoverflow.com is one of the top 50 websites in the world](https://www.alexa.com/siteinfo/stackoverflow.com). (That’s without even counting the Stack Exchange network, which is almost as big.) And every time I see a developer write code, they’ve got Stack Overflow open in one of their browser windows. Oh and—hey!—we do not make you sign up or pay to see the answers.

The company has been growing, too. Today we are profitable. We have almost 300 amazing employees worldwide and booked $70m in revenue last year. We have talent, advertising, and software products. The SaaS products (Stack Overflow for [Teams](https://stackoverflow.com/teams) and [Enterprise](https://stackoverflow.com/enterprise)) are growing at _200% a year_. That speaks to the fact that we’ve recruited an incredibly talented team that has produced such fantastic results. 

But, we have a lot of work ahead of us, and it’s going to take a different type of leader to get us through that work. 

The type of people Stack Overflow serves has changed, and now, as a part of the developer ecosystem, we have a responsibility to create an online community that is far more diverse, inclusive, and welcoming of newcomers.

In the decade or so since Stack Overflow started, the number of people employed as software developers [grew by 64%](https://www.bls.gov/careeroutlook/2019/data-on-display/projections-evaluation.htm?view_full) in the US alone. The field is going to keep growing everywhere in the world, and the demand for great software developers far outstrips supply. So a big challenge for Stack Overflow is welcoming those new developers into the fold. As I’ve [written](https://www.joelonsoftware.com/2018/04/23/strange-and-maddening-rules/):

> One thing I’m very concerned about, as we try to educate the next generation of developers, and, importantly, get more diversity and inclusiveness in that new generation, is what obstacles we’re putting up for people as they try to learn programming. In many ways Stack Overflow’s specific rules for what is permitted and what is not are obstacles, but an even bigger problem is rudeness, snark, or condescension that newcomers often see.
> 
> I care a lot about this. Being a developer gives you an unparalleled opportunity to [write the script for the future](https://www.joelonsoftware.com/2016/12/09/developers-are-writing-the-script-for-the-future/). All the flak that Stack Overflow throws in the face of newbies trying to become developers is actively harmful to people, to society, and to Stack Overflow itself, by driving away potential future contributors. And programming is hard enough; we should see our mission as making it easier.

The world has started taking a closer look at tech, and understanding that software and the internet are not just tools; they are shaping the future of society. Big tech companies are struggling with their place in the world. Stack Overflow is situated at the right place to be influential in how that future develops, and that is going to take a new type of leader.

new dog, too

It will not be easy to find a CEO who is the right person to lead that mission. We will, no doubt, hire one of those fancy executive headhunters to help us in the search. But, hey, this is Stack Overflow. If there’s one thing I have learned by now, it’s that there’s always someone in the community who can answer the questions I can’t. 

So we decided to put this announcement out there in hopes of finding great candidates that might have been under the radar. We’re especially focused on identifying candidates from under-represented groups, and making sure that every candidate we consider is deeply committed to making our company and community more welcoming, diverse, and inclusive.

Over the years, Fog Creek Software created several incredible hits and many wonderful memories along the way. It is great to watch Trello (under Michael Pryor) and Glitch (under Anil Dash) growing into enormously valuable, successful, and influential products with dedicated leaders who took these products much further than I ever could have, and personally I’m excited to see where Stack Overflow can go and turn my attention to the next thing.  

  * [Stack Overflow](https://www.joelonsoftware.com/category/reading-lists/stack-overflow/), [News](https://www.joelonsoftware.com/category/news/)

Hey, we have a new thing for you today!

Today’s new thing is called [Stack Overflow for Teams](https://stackoverflow.com/teams). It lets you set up a private place on Stack Overflow where you can ask questions that will only be visible to members of your team, company, or organization. It is a paid service, but it’s not expensive.

I meet people who use Stack Overflow every single day, but a lot of them tell me they have never needed to post their own question. “All the questions are already answered!” they say. Mission accomplished, I guess!

Still, when I think about what questions developers have every day, only the ones that have to do with public stuff can be asked on Stack Overflow. Maybe you don’t have a question about Python or Android… maybe you want to ask something about your team’s own code base!

That’s the idea behind Stack Overflow Teams.

[](https://i0.wp.com/www.joelonsoftware.com/wp-content/uploads/2018/05/Helicopters.png?ssl=1)

Quick background: every development team since the beginning of time has been trying to figure out how to get institutional knowledge out of people’s heads and into written, searchable form where everyone can find it. Like new members of the team. And old members of the team working on new parts of the code. And people who forgot what they did three years ago and now have questions about _their own code_.

For a while developers thought wikis might be the solution. Anyone who has used a wiki for this purpose has probably discovered that not very much knowledge actually makes it into the wiki, and what does is not particularly useful, doesn’t get updated, and honestly it just feels like a bunch of homework to write a bunch of wiki documentation about your code when you don’t know if it will ever help anyone.

Another solution being sold today is the idea of having some kind of online IRC-style chat rooms, and hoping that by searching those chat archives, you can find “institutional knowledge.” Ha ha ha! Even if that works, all you really find is the history of some conversation people had. It might have clues but it’s not knowledge.

But you know what does work? A Q&A system. Like Stack Overflow.

Why? Because unlike wikis, you don’t write documentation in the hopes that one day it might help someone. You answer questions that are going to help someone  _immediately._ And you can stop answering the minute you get the green checkmark that shows that you solved their problem.

And unlike chatrooms, searching actually works. It finds you a question and its answers, not a conversation-captured-in-amber.

This is why Stack Overflow worked so much better on the public internet than the previous generation of discussion forums, and we think that it will work for all the same reasons with teams’  _proprietary_ questions and answers.

When you join a team, you’ll see your team’s private questions right on [stackoverflow.com](https://stackoverflow.com/) (although they actually live in a separate database for security). Your teams are listed in the left hand navbar.

[](https://i0.wp.com/www.joelonsoftware.com/wp-content/uploads/2018/04/Teams1.png?ssl=1)

Everything else works pretty much … like you would expect. When you ask a question, you can direct it to your team or to the whole world. The UI makes it very clear whether you are posting publicly or privately. If you are asking a question of your team, there’s a _Notify_ field so you can type the names of some people who might be able to answer the question, and they’ll hear about it right away.

[](https://i0.wp.com/www.joelonsoftware.com/wp-content/uploads/2018/04/Teams2.png?ssl=1)

When you search, you can search everywhere, or just within your team. You can set up tags that are specific to your team, too.

The pricing is designed to be “no-brainer” pricing, starting at just $10 per month for the first ten users.

I think [Stack Overflow for Teams](https://stackoverflow.com/teams) is going to be almost as important to developers’ daily work as public Stack Overflow. It brings Stack Overflow’s uniquely powerful system to every developer question, not just the things that can be discussed in public. You can stop asking your teammates questions in email (where they help nobody else) or in chatrooms (where they are impossible to find) and start building your own private knowledge base to document your code and answer future teammates’ questions before they have them.

  * [News](https://www.joelonsoftware.com/category/news/)

There’s this popular idea among developers that when you face a problem with code, you should get out a rubber duck and explain, to the duck, exactly how your code was supposed to work, line by line, what you expected to see, what you saw instead, etc. Developers who try this report that the very act of explaining the problem in detail to an inanimate object often helps them find the solution.

[](https://meta.stackexchange.com/questions/308564/stack-exchange-has-been-taken-over-by-a-rubber-duck)This is one of many tricks to solving programming problems on your own. Another trick is [divide and conquer debugging](http://markheath.net/post/effective-debugging-with-divide-and-conquer). You can’t study a thousand lines of code to find the one bug. But you can divide them in half and quickly figure out if the problem happens in the first half or the second half. Keep doing this five or six times and you’ll pinpoint the single line of code with the problem.

It’s interesting, with this in mind, to read [Jon Skeet’s](https://stackoverflow.com/users/22656/jon-skeet?tab=profile) checklist for [writing the perfect question](https://codeblog.jonskeet.uk/2012/11/24/stack-overflow-question-checklist/). One of the questions Jon asks is “Have you read the whole question to yourself carefully, to make sure it makes sense and contains enough information for someone coming to it without any of the context that you already know?” That is essentially the Rubber Duck Test. Another question is “If your question includes code, have you written it as a short but complete program?” Emphasis on the  _short_ —that is essentially a test of whether or not you tried divide and conquer.

What Jon’s checklist can do, in the best of worlds, is to help people try the things that experienced programmers may have already tried, before they ask for help.

Sadly, not everybody finds his checklist. Maybe they found it and they don’t care. They’re having an urgent problem with code; they heard that Stack Overflow could help them; and they don’t have time to read some nerd’s complicated protocol for requesting help.

[](https://i0.wp.com/www.joelonsoftware.com/wp-content/uploads/2018/04/NYC.png?ssl=1)

One of the frequent debates about Stack Overflow is whether the site needs to be open to questions from programming novices.

When Jeff and I were talking about the initial design of Stack Overflow, I told him about this popular Usenet group for the C programming language in the 1980s. It was called [comp.lang.c.](https://groups.google.com/forum/#!forum/comp.lang.c)

C is a simple and limited programming language. [You can get a C compiler that fits in 100K.](http://repo.or.cz/w/tinycc.git) So, when you make a discussion group about C, you quickly run out of things to talk about.

Also. In the 1990s, C was a common language for undergraduates who were learning programming. And, in fact, said undergraduates would have [very basic problems](https://groups.google.com/forum/#!searchin/comp.lang.c/spolsky%7Csort:date/comp.lang.c/BKhAacGNtZI/GLSW-QG_O3MJ) in C. And they might show up on comp.lang.c asking their questions.

And the old-timers on comp.lang.c were bored.  _So_ bored. Bored of the undergraduates showing up every September wondering why they can’t return a local char array from a function et cetera, et cetera, ad nauseum. Every damn September.

The old timers invented the concept of FAQs. They used them to say “please don’t ask things that have been asked before, ever, in the history of Usenet” which honestly meant that the only questions they really wanted to see were so bizarre and so esoteric that they were really enormously boring to 99% of working C programmers. The newsgroup languished because it catered only to the few people that had been there for a decade.

Jeff and I talked about this. What did we think of newbie questions?

We decided that newbies had to be welcome. Nothing was too “beginner” to be a reasonable question on Stack Overflow… as long as you did some homework before asking the question.

We understood that this might mean that some of the more advanced people might grow bored with duplicate, simple questions, and move on. We thought that was fine: Stack Overflow doesn’t have to be a lifetime commitment. You’re welcome to get bored and move on if you think that the newbies keep asking why they can’t return local char arrays (“but it works for me!”) and you would rather devote the remaining short years of your life to something more productive, like sorting your record albums.

The mere fact that you are a newbie doesn’t mean that your question doesn’t belong on Stack Overflow. To prove the point, I asked “[How do you move the turtle in Logo](https://stackoverflow.com/questions/1003841/how-do-i-move-the-turtle-in-logo),” hoping to leave behind evidence that the site designers wanted to allow absolute beginners.

Thanks to the law of unintended consequences, this caused a lot of brouhaha, but not because the question was too easy. The real problem there was that I was asking the question in bad faith. Jeff Atwood [explained](https://meta.stackexchange.com/questions/158289/why-is-the-how-to-move-the-turtle-in-logo-question-closed#comment457933_158334) it: “Simple is fine. No effort and research is not.” ([Also this](https://en.wikipedia.org/wiki/Wikipedia:Do_not_disrupt_Wikipedia_to_illustrate_a_point).)

[](https://i0.wp.com/www.joelonsoftware.com/wp-content/uploads/2018/04/StBarts.png?ssl=1)

To novices, the long bureaucratic rigmarole associated with asking your first question on Stack Overflow can feel either completely unnecessary, or just plain weird. It’s like Burning Man. You just want to go to a nice glittery dance party in the desert, but the Burning People are yammering on about their goddamn [10 principles](https://burningman.org/culture/philosophical-center/10-principles/), and “radical self-expression” and so on and so forth, and _therefore_ after washing your dishes you must carefully save the dirty dishwater like a cherished relic and remove every drop of it from the Playa, bringing it home with you, in your check-in luggage if necessary. Every community has lots of rules and when you join the community they either seem strange and delightful or, if you’re just desperately trying to get some code to work, they are strange and maddening.

A lot of the rules that are important to make Burning Man successful are seemingly arbitrary, but they’re still necessary. The US Bureau of Land Management which makes the desert available for Burning Man requires that no contaminated water be poured out on the ground because the clay dirt doesn’t really absorb it so well and it can introduce all kinds of disease and whatnot, but who cares because Burning Man simply will not be allowed to continue if the participants don’t pack out their used water.

Similarly for Stack Overflow. We don’t allow, say, questions that are too broad (“How do I make a program?”). Our general rule is that if the correct length of an answer is _a whole book_ you are asking too much. These questions feel like showing up on a medical website and saying something like “I think my kidney has been hurting. How can I remove it?” It’s crazy—and incidentally, insulting to the people who spent ten years in training learning to be surgeons.

One thing I’m very concerned about, as we try to educate the next generation of developers, and, importantly, get more diversity and inclusiveness in that new generation, is what obstacles we’re putting up for people as they try to learn programming. In many ways Stack Overflow’s specific rules for what is permitted and what is not are obstacles, but an even bigger problem is rudeness, snark, or condescension that newcomers often see.

I care a lot about this. Being a developer gives you an unparalleled opportunity to [write the script for the future](https://www.joelonsoftware.com/2016/12/09/developers-are-writing-the-script-for-the-future/). All the flak that Stack Overflow throws in the face of newbies trying to become developers is actively harmful to people, to society, and to Stack Overflow itself, by driving away potential future contributors. And programming is hard enough; we should see our mission as making it easier.

We’re planning a lot of work in this area for the next year. We can’t change everybody and we can’t force people to be nice. But I think we can improve some aspects of the Stack Overflow user interface to encourage better behavior, for example, we could improve the prompts we provide on the “Ask Question” page, and we could provide more tools for community moderation of comments where the snark currently runs unchecked.

[](https://i0.wp.com/www.joelonsoftware.com/wp-content/uploads/2018/04/2016-09-10-21.38.14-1.jpg?ssl=1)

We’re also working on new features that will let you direct your questions to a private, smaller group of people on your own team, which may bring some of the friendly neighborhood feel to the big city of Stack Overflow.

Even as we try to make Stack Overflow more friendly, our primary consideration at Stack Overflow has been to build the world’s greatest resource for software developers. The average programmer, in the world, has been helped by Stack Overflow 340 times. That’s the real end-game here. There are other resources for learning to program and getting help, but there’s only one site in the world that developers trust this much, and that is worth preserving—the programming equivalent to the Library of Congress.

  * [News](https://www.joelonsoftware.com/category/news/)

_[This is the second in a series of posts about Stack Overflow. The first one is[The Stack Overflow Age](https://www.joelonsoftware.com/2018/04/06/the-stack-overflow-age/).]_

Around 2010 the success of Stack Overflow had led us into some conversations with VCs, who wanted to invest.

The firm that eventually invested in us, [Union Square Ventures](https://www.usv.com/), told us that they were so excited by the power of gamification that they were only investing in companies that incorporated some kind of game play.

For example, Foursquare. Remember Foursquare? It was all about making your normal post-NYU life of going to ramen noodle places and dive bars into a fun game that incidentally generated wads of data for marketers. Or Duolingo, which is a fun app with flash cards that teaches you foreign languages. Those were other USV investments from that time period.

At the time, I had to think for a minute to realize that Stack Overflow has “gamification” too. Not a ton. Maybe a _dusting_ of gamification, most of it around reputation.

Stack Overflow reputation started as a very simple score. The original idea was just that you would get 10 points when your answers were upvoted. Upvotes do two things. They get the most useful answers to the top, signaling that other developers who saw this answer thought it was good. They also send the person who wrote the answer a real signal that their efforts helped someone. This can be incredibly motivating.

You would lose points if your questions were downvoted, but you actually only lose 2 points. We didn’t want to punish you so much as we wanted to show other people that your answer was wrong. And to avoid abuse, we actually make you  _pay_ one reputation point to downvote somebody, so you better really mean it. That was pretty much the whole system.

Now, this wasn’t an original idea. It was originally inspired by Reddit Karma, which started out as an integer that appeared in parentheses after your handle. If you posted something that got upvoted, your karma went up as a “reward.” That was it. Karma [didn’t do a single thing](https://www.zdnet.com/article/collaborative-filtering-comparing-reddits-karma-system-to-digg/) but still served as a system for reward and punishment.

What reputation and karma do is send a message that this is a community with norms, it’s not just a place to type words onto the internet. (That would be 4chan.) We don’t really exist for the purpose of letting you exercise your freedom of speech. You can get your freedom of speech somewhere else. Our goal is to get the best answers to questions. All the voting makes it clear that we have standards, that some posts are better than others, and that the community itself has some norms about what’s good and bad that they express through the vote.

It’s not a perfect system (more on the problems in a minute), but it’s a reasonable first approximation.

By the way, Alexis Ohanian and Steve Huffman, the creators of Reddit, were themselves inspired by a more primitive karma system, on Slashdot. This system had real-world implications. You didn’t get karma so that other people could see your karma; you got karma so that the system knew you weren’t a spammer. If a lot of your posts had been flagged for abuse, your karma would go down and you might lose posting or moderation privileges. But you weren’t really supposed to show off your high karma. “Don’t worry too much about it; it’s just an integer in a database,” Slashdot told us.

To be honest, it was initially surprising to me that you could just print a number after people’s handles and they would feel rewarded. Look at me! Look at my four digit number! But it does drive a tremendous amount of good behavior. Even people who aren’t participating in the system (by working to earn reputation) buy into it (e.g., by respecting high-reputation users for their demonstrated knowledge and helpfulness).

But there’s still something of a mystery here, which is why earning “magic internet points” is appealing to anyone.

I think the answer is that it’s nice to know that you’ve made a difference. You toil away in the hot kitchen all day and when you serve dinner it’s nice to hear a compliment or two. If somebody compliments you on the extra effort you put into making radish roses, you’re going to be very happy.

This is a part of a greater human need: to make an impact on the world, and to know that you’re contributing and being appreciated for it. Stack Overflow’s reputation system serves to recognize that you’re a human being and we are super thankful for your contribution.

That said, there is a dark side to gamification. It’s not 100% awesome.

The first problem we noticed is that it’s very nice to get an upvote, but getting a downvote feels like a slap in the face. Especially if you don’t understand why you got the downvote, or if you don’t agree. Stack Overflow’s voting has made many people unhappy over the years, and there are probably loads of people who felt unwelcome and who don’t participate in Stack Overflow as a result. (Here’s an old blog post explaining [why we didn’t just eliminate downvotes](https://stackoverflow.blog/2009/03/09/the-value-of-downvoting-or-how-hacker-news-gets-it-wrong/)).

There’s another problem, which is that, to the extent that the gamification in Stack Overflow makes the site feel less inclusive and welcoming to many people, it is disproportionately off-putting to programmers from underrepresented groups. While Stack Overflow does have many amazing, high reputation contributors who are women or minorities, we’ve also heard from too many who were apprehensive about participating.

These are big problems. There’s a lot more we can and will say about that over the next few months, and we’ve got a lot of work ahead of us trying to make Stack Overflow a more inclusive and diverse place so we can improve the important service that it provides to developers everywhere.

Gamification can shape behavior. It can guide you to do certain things in certain ways, and it can encourage certain behaviors. But it’s a very weak force. You can’t do that much with gamification. You certainly can’t get people to do something that they’re not interested in doing, anyway. I’ve heard a lot of crazy business plans that are pinning rather too high hopes on gamification as a way of getting people to go along with some crazy scheme that the people won’t want to go along with. Nobody’s going to learn French just to get the Duolingo points. But if you are learning French, and you are using Duolingo, you might make an effort to open the app every day just to keep your streak going.

I’ve got more posts coming! The next one will be about the obsessive way Stack Overflow was designed for the artifact, in other words, we optimized everything to create amazing results for developers with problems arriving from Google, not just to answer questions that people typed into our site.
  *[ M1]: The first generally available Apple CPU ("Apple Silicon") for laptops with 4 Firestorm and 4 Icestorm cores.
  *[uop]: Micro-operation: instructions are translated into one or more uops, which are simple operations executed by the CPU's execution units.
  *[macro-fuse]: The fusing of an ALU operation and subsequent jump, such as `dec eax; jnz label` into one operation
  *[macro-fused]: The fusing of an ALU operation and subsequent jump, such as `dec eax; jnz label` into one operation
  *[uarch]: Microarchitecture: a specific implementation of an ISA, e.g., "Haswell microarchitecture".
  *[p1]: port 1 (GP and SIMD ALU, integer mul)
  *[p6]: port 6 (GP ALU, all branches)
  *[immediate]: When discussing assembly instructions an immediate is a value embedded in the instruction itself, e.g., the 1 in add eax, 1.
  *[p5]: port 5 (GP and SIMD ALU, vector shuffles)
  *[p0]: port 0 (GP and SIMD ALU, not-taken branches)
  *[M1]: The first generally available Apple CPU ("Apple Silicon") for laptops with 4 Firestorm and 4 Icestorm cores.
  *[naturally aligned]: Naturally aligned data is data whose location in memory is a multiple of its size, e.g., a 4 byte element whose address is a multiple of 4 bytes.
  *[AGU]: Address Generation Unit
  *[p2]: port 2 (load/store AGU)
  *[p3]: port 3 (load/store AGU)
  *[p7]: port 7 (limited store AGU)
  *[CNL]: Intel's Cannon Lake (client) architecture, the i3-8121U was the only SKU ever released
  *[SKX]: Intel's Skylake (server) architecture including Skylake-SP, Skylake-X and Skylake-W
  *[SKL]: Intel's Skylake (client) architecture, aka 6th Generation Intel Core i3,i5,i7
  *[HSW]: Intel's Haswell architecture, aka 4th Generation Intel Core i3,i5,i7
  *[out-of-order]: Out-of-order execution allows CPUs to execute instructions out of order with respect to the source.
  *[MSROM]: Intel's name for the microcode engine: a component handles complex instructions which require more than 4 uops using microcode which feeds uops directly into the IDQ.
  *[MITE]: Intel's name for the "legacy" decoder, i.e., the decoder that usually decodes instructions when they are not found in the MSROM.
  *[microcode]: Internal instructions and other logic forming part of a CPU which may be used to implement user-visible instructions and control other aspects of CPU behavior and which may be modified dynamically by vendor-provided updates.
  *[LSD]: Lysergic acid diethylamide or Loop stream detector, but in the context of this blog probably the latter: The so-called loop buffer that can cache small loops of up to ~64 uops on recent Intel architectures. Not actually a separate structure: the hardware justs locks the loop down in the IDQ.
  *[basic block]: a straight-line code sequence with no branches in except to the entry and no branches out except at the exit (Wikipedia).
  *[OoO]: Out-of-order execution allows CPUs to execute instructions out of order with respect to the source.
  *[Sunny Cove]: The new 7nm microarchitecture used in Ice Lake CPUs.
  *[Firestorm]: The big, high IPC cores in the Apple M1 CPU.
  *[Icestorm]: The low power efficiency cores in the Apple M1 CPU.
  *[ROB]: Re-order buffer: n ordered buffer which stores in-progress instructions on an out-of-order processor.
  *[IPC]: Instructions per cycle: calculated over an interval by measuring the number of instructions executed and the duration in cycles.
  *[MLP]: Memory level parallelism: having multiple misses to memory outstanding from a single core. When used as a metric, it refers to the average number of outstanding requests over some period.
  *[demand load]: A true load that appears in the source code or assembly, as opposed to loads initiated by software or hardware prefetch.
  *[PRF]: Physical register file: The hardware registers used for renaming architectural (source visible) registers, usually much larger in number than the architectural register count.
  *[SIMD]: Single Instruction Multiple Data: an ISA type or ISA extension like Intel's AVX or ARM's NEON that can perform multiple identical operations on elements packed into a SIMD register.
  *[GP]: General purpose: as opposed to SIMD or FP. On x86 often refers to instructions such as integer addition, or registers such as eax.
  *[delamination]: An situation where an instruction using an indexed addressing mode, that is otherwise eligible for micro-fusion, stays fused in the uop-cache, but then delaminates into two separate uops prior to issue, and so counts as two against the pipeline (rename) limit of four uops.
  *[IDQ]: Queue that collects incoming instructions from the decoder, uop cache or microcode engine and delivers them to the renamer (RAT).
  *[RMW]: Read-modify-write: an instruction that reads from a memory location, operates on the value, and writes the result back to the same location.