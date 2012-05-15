[accomplishment]
// ACCOMPLISHMENT: On Planet Ubuntu ('title' field)
// .
// ENGLISH TRANSLATION:
// On Planet Ubuntu

// .
// ----- TRANSLATION INSTRUCTIONS ----- 
// A short description of the accomplishment.
//          NOTE: Describe this in the past tense as if it has been achieved (e.g. Registered On Launchpad). 
_("blog-on-planet-ubuntu_title")
// ACCOMPLISHMENT: On Planet Ubuntu ('description' field)
// .
// ENGLISH TRANSLATION:
// You have a blog on Planet Ubuntu

// .
// ----- TRANSLATION INSTRUCTIONS ----- 
// Add a descriptive single-line summary of the accomplishment.
_("blog-on-planet-ubuntu_description")
// ACCOMPLISHMENT: On Planet Ubuntu ('summary' field)
// .
// ENGLISH TRANSLATION:
// <a href="http://planet.ubuntu.com">Planet Ubuntu</a> is a website that lists blogs (personal websites) of people involved in the Ubuntu project and our various flavors.
// Planet Ubuntu has become a very popular resource for our community and beyond to keep up to date with what is happening in the project. It brings together many, many blogs from across the community and the world into a single webpage that is convenient for browsing.
// Planet Ubuntu works by users adding their blog's RSS feeds (most blogs have an RSS feed that you can use) which will take just the content from the blog and embed it into Planet Ubuntu.
// To have your blog listed on Planet Ubuntu you need to first become an <i>Ubuntu Member</i>.

// .
// ----- TRANSLATION INSTRUCTIONS ----- 
// Introduce the accomplishment, explain what the different concepts are that are involved, and provide guidance on how to accomplish it.
//          NOTE: Break this into paragraphs by putting each paragraph on a new line. 
//          FORMATTING ALLOWED: <i> <strong> <tt>
_("blog-on-planet-ubuntu_summary")
// ACCOMPLISHMENT: On Planet Ubuntu ('steps' field)
// .
// ENGLISH TRANSLATION:
// You should first ensure that you have an SSH key added to Launchpad. Read more how to do this <a href="https://help.launchpad.net/YourAccount/CreatingAnSSHKeyPair">here</a>.
// You will need to install the <tt>bzr</tt> tool. You can do this in the Ubuntu Software Center.
// Tell <tt>bzr</tt> your name and email address. It's best to use an email address associated with your Launchpad account: <tt>bzr whoami "Example User <user@example.com>"</tt>
// Now login to Launchpad: <tt>bzr launchpad-login yourusername</tt>
// Now use <tt>bzr</tt> to download the Planet Ubuntu branch: bzr checkout lp:~planet-ubuntu/config/main planet-ubuntu
// You will need to create small image called a <i>Hackergotchi</i> (this is usually of your head). This should be about 100x100 pixels in size. Copy it to the heads directory and ensure the filename is your username: <tt>cp ~/hackergotchi.png heads/yourusername.png</tt>
// Now add your hackergotchi to the branch: <tt>bzr add heads/yourusername.png</tt>
// Now add the end of the <tt>config.ini</tt> file add a line for your blog in square brackets: e.g. <tt>[[http://blog.example.com/~yourusername/feed?category=ubuntu-only]]</tt>
// Underneathe that add your name: <tt>name = Your Name Here</tt>
// Underneathe that add your hackergotchi filename: <tt>face = yourusername.png</tt>
// Underneathe that add your Launchpad username: <tt>nick = yourusername</tt>
// Now check that your changes look good: <tt>bzr diff</tt>
// Finally, commit it to the branch: <tt>bzr commit -m "Added yourusername to Planet Ubuntu"</tt>

// .
// ----- TRANSLATION INSTRUCTIONS ----- 
// Add a series of step-by-step instructions for how to accomplish this trophy.
//          NOTE: Put each step on a new line
//          FORMATTING ALLOWED: <i> <strong> <tt>
_("blog-on-planet-ubuntu_steps")
// ACCOMPLISHMENT: On Planet Ubuntu ('tips' field)
// .
// ENGLISH TRANSLATION:
// The <a href="http://www.ubuntu.com/project/about-ubuntu/conduct">Ubuntu Code of Conduct</a> applies to all actions by Ubuntu members, including posting to their blogs.
// As a rule of thumb, English should be considered the "lingua franca" of Planet Ubuntu. There are a number of language and locale specific Planets run by Ubuntu LoCo Teams, which are a great way for teams to get news out in their local language. However, the official Ubuntu Planet should attempt to use English where possible to reach the widest possible audience.
// Ubuntu members who publish blogs on Planet Ubuntu should endeavour to ensure that company confidential information is not posted there. The planet administrators will make a reasonable judgement about the sensitivity of information in blogs re-published there, and will consider requests for the removal of content on those grounds. However, we cannot guarantee that we will be able to establish the confidentiality of any given piece of information, and will not automatically remove posts on request.
// If you do need something removing, you can contact the sysadmin team at <a href="mailto:rt@ubuntu.com">rt@ubuntu.com</a>.

// .
// ----- TRANSLATION INSTRUCTIONS ----- 
// Add tips and best practise for accomplishing this trophy.
//          NOTE: Put each tip on a new line
//          FORMATTING ALLOWED: <i> <strong> <tt>
_("blog-on-planet-ubuntu_tips")
// ACCOMPLISHMENT: On Planet Ubuntu ('pitfalls' field)
// .
// ENGLISH TRANSLATION:
// Don't let a difference of style or opinion spiral into a conflict which will make it impossible for you to collaborate with others on matters of mutual interest. No single "set of rules" would let us all get along - but we expect everyone in the Ubuntu community to make a real effort to treat one another respectfully, across great cultural divides.

// .
// ----- TRANSLATION INSTRUCTIONS ----- 
// Add things the user should not do when working to accomplish this trophy.
//          NOTE: Put each pitfall on a new line
//          FORMATTING ALLOWED: <i> <strong> <tt>
_("blog-on-planet-ubuntu_pitfalls")
// ACCOMPLISHMENT: On Planet Ubuntu ('links' field)
// .
// ENGLISH TRANSLATION:
// http://planet.ubuntu.com
// https://wiki.ubuntu.com/PlanetUbuntu

// .
// ----- TRANSLATION INSTRUCTIONS ----- 
// Add related web addresses (don't include a HTML link).
//          NOTE: Put each URL on a new line
_("blog-on-planet-ubuntu_links")
// ACCOMPLISHMENT: On Planet Ubuntu ('help' field)
// .
// ENGLISH TRANSLATION:
// #ubuntu-community-team on Freenode

// .
// ----- TRANSLATION INSTRUCTIONS ----- 
// Add related help resources (e.g. IRC channel names).
//          NOTE: Put each help resource on a new line
//          FORMATTING ALLOWED: <i> <strong> <tt>
_("blog-on-planet-ubuntu_help")
