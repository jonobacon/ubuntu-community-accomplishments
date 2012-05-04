[accomplishment]
// ACCOMPLISHMENT: Imported an SSH Key ('title' field)
// .
// ENGLISH TRANSLATION:
// Imported an SSH Key

// .
// ----- TRANSLATION INSTRUCTIONS ----- 
// A short description of the accomplishment.
//          NOTE: Describe this in the past tense as if it has been achieved (e.g. Registered On Launchpad). 
_("imported-ssh-key_title")
// ACCOMPLISHMENT: Imported an SSH Key ('description' field)
// .
// ENGLISH TRANSLATION:
// You have imported an SSH key into launchpad.

// .
// ----- TRANSLATION INSTRUCTIONS ----- 
// Add a descriptive single-line summary of the accomplishment.
_("imported-ssh-key_description")
// ACCOMPLISHMENT: Imported an SSH Key ('summary' field)
// .
// ENGLISH TRANSLATION:
// An SSH key secures the connection between your computer and Launchpad while you're pushing Bazaar branches up to Launchpad. To push code branches to Launchpad you first need to generate your SSH key. The key is made up of two parts: a private key that stays on your computer and a public key that you register with Launchpad.

// .
// ----- TRANSLATION INSTRUCTIONS ----- 
// Introduce the accomplishment, explain what the different concepts are that are involved, and provide guidance on how to accomplish it.
//          NOTE: Break this into paragraphs by putting each paragraph on a new line. 
//          FORMATTING ALLOWED: <i> <strong> <tt>
_("imported-ssh-key_summary")
// ACCOMPLISHMENT: Imported an SSH Key ('steps' field)
// .
// ENGLISH TRANSLATION:
// Install OpenSSH. You can install OpenSSH by opening your terminal and typing: <tt>sudo apt-get install openssh-client</tt>.
// Once OpenSSH is installed, stay in the terminal and type: <tt>ssh-keygen -t rsa</tt>.
// When prompted, press Enter to accept the default file name for your key.
// Next, enter then confirm a password to protect your SSH key. Your key pair is stored in <tt>~/.ssh/</tt> as <tt>id_rsa.pub</tt> (public key) and id_rsa (private key).
// Open your public key in a text editor and copy its contents to your clipboard. The public key file has the extension <tt>.pub</tt>. For example: <tt>id_rsa.pub</tt>.
// Visit your Launchpad SSH keys page.
// Paste your public key into the text box and then click the <b>Import public key</b> button to continue.

// .
// ----- TRANSLATION INSTRUCTIONS ----- 
// Add a series of step-by-step instructions for how to accomplish this trophy.
//          NOTE: Put each step on a new line
//          FORMATTING ALLOWED: <i> <strong> <tt>
_("imported-ssh-key_steps")
// ACCOMPLISHMENT: Imported an SSH Key ('links' field)
// .
// ENGLISH TRANSLATION:
// https://help.launchpad.net/YourAccount/CreatingAnSSHKeyPair

// .
// ----- TRANSLATION INSTRUCTIONS ----- 
// Add related web addresses (don't include a HTML link).
//          NOTE: Put each URL on a new line
_("imported-ssh-key_links")
// ACCOMPLISHMENT: Imported an SSH Key ('help' field)
// .
// ENGLISH TRANSLATION:
// #launchpad on Freenode

// .
// ----- TRANSLATION INSTRUCTIONS ----- 
// Add related help resources (e.g. IRC channel names).
//          NOTE: Put each help resource on a new line
//          FORMATTING ALLOWED: <i> <strong> <tt>
_("imported-ssh-key_help")
