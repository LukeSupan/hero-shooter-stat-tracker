# Hero Shooter Stat Tracker
This was designed with **Overwatch** and **Marvel Rivals** in mind.
>I'd recommend not combining the two games in your doc. If you play both have one for MR and one for Overwatch. The MVP stat is pretty much lost when you do that.
---


## Match Entry Formatting:
```
tank,tank2/dps1,dps2/support1,support2/win(orloss)
```

- **commas**(``,``) are separators for multiple players in a role.
- **slashes**(``/``) are separators for different roles.
- you do **NOT** need to fill all slots.
- Use `none` to fill slots that have a random.
- One game per line, then go to a newline, each line should end with either win or loss. Ignore draws.

## Examples
```
luke/mar/kayla/win
none/mar/kayla/loss
none/luke,mar/kayla/win
luke,mar/aiden,ray/kayla,dalton/win
```

## Marvel Rivals specifics
If you are playing marvel rivals or want to add a mvp for whatever reason use:
```
luke(mvp),aiden/mar/kayla/win
```
In this case, luke is the MVP. You simply add (mvp) after the name with no spaces
I treat mvp and svp the same, just say mvp. you can see the win loss ratio for mvps which shows SVP. It's just easier to use exclusively mvp for recording data
