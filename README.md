## iou.py ##
Quick _(read: very poorly organized and hackish code)_ IOU python script to handle debts owed.

Three commands are supported: `new`, `history`, and `summary`.

`new`
---

`new` is used to create a new transaction. The transaction must be formatted as such:

`[name] owes me $[amount] for [memo]`
**or**
`I owe [name] $[amount] for [memo]`

Example:

```
$ python3 iou.py new
$ Enter transaction details: I owe Dad $10.50 for gas money
```

`history`
---

`history` `[name]` is used to list out all transactions made. If `name` is specified, then only transactions with the person specified will be listed.

Example:

```
$ python3 iou.py history
You owed Dad $10.5 for gas money
```

`summary`
---

`summary` `[name]` is used to list out the total amount of money owed to each person. If `name` is specified, then only the total with the person specified will be listed.

Example:

```
$ python3 iou.py summary
You owe Dad $10.5
```

---

To make the command available anywhere, just add the following to your `.bash_profile` or `.bashrc`:

`alias iou='function _iou() { eval "python3 ~/workspace/scratch/iou.py $*"; };_iou'`

Usage:

```
$ iou history
$ iou summary
```
