# Solution

(My keyboard layout is broken. I can rewrite this in swedish later.)

You try to make an xss using the xss-parameter on the /chall page, but you soon realize that it won't work.

In the source of the page you discover that you can see the source code at /source and that there is another parameter called debug.

But in the source code you also see that this new parameter is also filtered. Hmm.....

You see that when the puppet runs it clicks the button while interacting with the page. So you look at the debug-parameter again.

Finally you realize that the filtering is broken since it is done in reverse order. It is escapeJS(escapeHTML(...)) but it should be the other way around.

So by sending debug as `'+alert(1));//` an alert box will trigger when the button is pressed.

http://localhost:3000/chall?xss=abc&debug=%27%2Balert%281%29%29%3B%2F%2F

https://gchq.github.io/CyberChef/#recipe=URL_Encode(true)&input=JythbGVydCgxKSk7Ly8
