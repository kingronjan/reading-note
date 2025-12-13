From: [linux - Use Expect in a Bash script to provide a password to an SSH command - Stack Overflow](https://stackoverflow.com/a/28293259/16499496)



```bash
#!/usr/bin/expect

set timeout 20

set cmd [lrange $argv 1 end]
set password [lindex $argv 0]

eval spawn $cmd
expect "assword:"   # matches both 'Password' and 'password'
send -- "$password\r"; # -- for passwords starting with -, see https://stackoverflow.com/a/21280372/4575793
interact
```

Put it to `/usr/bin/exp`, then you can use:

- `exp <password> ssh <anything>`
- `exp <password> scp <anysrc> <anydst>`

Done!