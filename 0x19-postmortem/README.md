### 0x19-postmortem
* Any software system will eventually fail, and that failure can come stem from a wide range of possible factors: bugs, traffic spikes, security issues, hardware failures, natural disasters, human error… Failing is normal and failing is actually a great opportunity to learn and improve. Any great Software Engineer must learn from his/her mistakes to make sure that they won’t happen again. Failing is fine, but failing twice because of the same issue is not.

* A postmortem is a tool widely used in the tech industry. After any outage, the team(s) in charge of the system will write a summary that has 2 main goals:

- To provide the rest of the company’s employees easy access to information detailing the cause of the outage. Often outages can have a huge impact on a company, so managers and executives have to understand what happened and how it will impact their work.
- And to ensure that the root cause(s) of the outage has been discovered and that measures are taken to make sure it will be fixed.

* Postmortem *
 - Upon the release of Alx School's System Engineering & DevOps project 0x19, approximately 00:07 Pacific Standard Time (PST), an outage occurred on an isolated Ubuntu 14.04 container running an Apache web server. GET requests on the server led to 500 Internal Server Error's, when the expected response was an HTML file defining a simple Alx WordPress site.

* Debugging Process

encountered the issue upon opening the project and being, well, instructed to address it, roughly 19:20 PST. He promptly proceeded to undergo solving the problem.

1. Checked running processes using ps aux. Two apache2 processes - root and www-data - were properly running.

2. Looked in the sites-available folder of the /etc/apache2/ directory. Determined that the web server was serving content located in /var/www/html/.

3. In one terminal, ran strace on the PID of the root Apache process. In another, curled the server. Expected great things... only to be disappointed. strace gave no useful information.

4. Repeated step 3, except on the PID of the www-data process. Kept expectations lower this time... but was rewarded! strace revelead an -1 ENOENT (No such file or directory) error occurring upon an attempt to access the file /var/www/html/wp-includes/class-wp-locale.phpp.

5. Looked through files in the /var/www/html/ directory one-by-one, using Vim pattern matching to try and locate the erroneous .phpp file extension. Located it in the wp-settings.php file. (Line 137, require_once( ABSPATH . WPINC . '/class-wp-locale.php' );).

6. Removed the trailing p from the line.

7. Tested another curl on the server. 200 A-ok!

8. Wrote a Puppet manifest to automate fixing of the error.

* Summation
In short, a typo. Gotta love'em. In full, the WordPress app was encountering a critical error in wp-settings.php when tyring to load the file class-wp-locale.phpp. The correct file name, located in the wp-content directory of the application folder, was class-wp-locale.php.

Patch involved a simple fix on the typo, removing the trailing p.
* Prevention
This outage was not a web server error, but an application error. To prevent such outages moving forward, please keep the following in mind.
 - Test! Test test test. Test the application before deploying. This error would have arisen and could have been addressed earlier had the app been tested.

- Status monitoring. Enable some uptime-monitoring service such as UptimeRobot to alert instantly upon outage of the website.

Note that in response to this error, I wrote a Puppet manifest 0-strace_is_your_friend.pp to automate fixing of any such identitical errors should they occur in the future. The manifest replaces any phpp extensions in the file /var/www/html/wp-settings.php with php.
