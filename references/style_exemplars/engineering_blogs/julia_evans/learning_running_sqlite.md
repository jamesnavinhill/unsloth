# Learning a few things about running SQLite

**Source**: [https://jvns.ca/blog/2026/07/17/learning-about-running-sqlite/](https://jvns.ca/blog/2026/07/17/learning-about-running-sqlite/)  
**Style Profile**: Delightfully approachable curiosity, demystifying complex technical machinery

---

Hello! I’ve been working on a Django site recently, and I decided to use SQLite as the database. When I was getting started with using SQLite as database for a website I read a [bunch](https://alldjango.com/articles/definitive-guide-to-using-django-sqlite-in-production) of blog posts about how it is totally fine to use SQLite in production for a small site and I think it _is_ totally fine, but what I did not fully appreciate is that SQLite is still a database, databases are complicated, and I do not know a lot about operating databases.

So here are a couple of small things I’ve been learning about running SQLite. This is the 4th website I’ve used SQLite for, and I think this one is harder because with the power of the Django ORM I’ve been making the database do more work than I was previously without Django.

I started by turning on WAL mode like all the blog posts said to do and hoping for the best.

###  `ANALYZE` is apparently important 

Today I was running a query (using [SQLite’s FTS5](https://www.sqlite.org/fts5.html) for full-text search) on a table with 4000 rows and it took 5 seconds. That seemed wrong to me: computers are fast!

It turned out that what I needed to do was to run [`ANALYZE`](https://sqlite.org/lang_analyze.html)! Immediately the problem query went from taking 5 seconds to like 0.05 seconds (or some other number small enough that I didn’t care to investigate further). I still don’t know exactly what went wrong in the query plan, but my best guess is that it was some sort of [accidentally quadratic](https://accidentallyquadratic.tumblr.com/) thing.

`ANALYZE` generates “statistics” (I guess about the number of rows in each table? and presumably other things?) so that the query planner can make better choices.

Maybe one day I’ll learn to read a query plan.

###  cleaning up the database is tricky 

Occasionally I’ve run into situations where I accidentally put a bunch of rows in my database that I don’t want to be there (for example completed tasks from [django-tasks-db](https://github.com/RealOrangeOne/django-tasks-db)), and I want to clean them up.

What’s happened to me a few times in this case is:

  1. I run some kind of command to clean up the rows
  2. The command takes more than 5 seconds, since there are a lot of rows (though I still have some questions about why these DELETE statements are so slow honestly, maybe there’s a bunch of Python code running inside a transaction, I’m not sure)
  3. One of the other workers tries to write the database while this is happening, and times out after 5 seconds (I have a timeout of 5 seconds set)
  4. The worker crashes because it couldn’t write to the database and the VM shuts down

My approach so far has been to just do these cleanup operations in small batches so that I don’t need to do database queries that take more than 5 seconds to run. This whole experience has given me more of an appreciation for why someone might want to use a “real” database like Postgres which can have more than one writer at the same time though.

Maybe in the future I’ll just take the site down for scheduled maintenance instead when I need to do this kind of thing, but I haven’t figured out a workflow for that yet.

###  no notes on performance of ORM queries yet 

So far I’ve been using Django’s ORM to make any query I want without paying any attention at all to query performance and it’s mostly been going okay other than the `ANALYZE` thing. The database is pretty small (maybe 10000 rows?) and I expect it to stay pretty small forever, so I’m hoping that that plan will keep working.

###  backing up sqlite 

I’ve done SQLite backups a couple of ways. I don’t think I’ve actually tested restoring from my backups but I do usually try to monitor them with a dead man’s switch.

**way 1: restic**
    
    
    sqlite3 /data/calendar.db "VACUUM INTO '/tmp/calendar.sqlite'"
    gzip /tmp/calendar.sqlite
    
    # Upload backup to S3
    # Sometimes the backup gets OOM killed and so it stays locked, do an unlock
    restic -r s3://s3.amazonaws.com/some_bucket/ unlock
    # Do the backup & prune old backups
    restic -r s3://s3.amazonaws.com/some_bucket/ backup /tmp/calendar.sqlite.gz
    restic -r s3://s3.amazonaws.com/some_bucket/ snapshots
    restic -r s3://s3.amazonaws.com/some_bucket/ forget -l 1 -H 6 -d 2 -w 2 -m 2 -y 2
    restic -r s3://s3.amazonaws.com/some_bucket/ prune
    

**way 2:[litestream](https://litestream.io/)**

I started trying out Litestream recently because I felt like doing incremental backups might be more efficient: my restic backups were sometimes getting OOM killed, and I was a bit tired of it. Basically I just write a config file and run:
    
    
    litestream replicate -config litestream.yml
    

I set `retention: 400h` in my config file in an attempt to retain some amount of history of the database but I have no idea if it works.

I’ve been backing up to AWS, which is always a pain because it’s annoying to navigate the AWS console to generate credentials. Maybe one day I’ll move away to some other S3-compatible alternative.

###  you can use multiple databases 

My current project only has one database, but one trick I used with [Mess with DNS](https://messwithdns.net/) was to split the tables into three separate database files because I didn’t actually need my tables to be in the same db. I think it was helpful.

Mess with DNS has been running on SQLite for 4 years now (since 2022) and it’s been great, I think the move from Postgres was a great choice for that project.

###  that’s all! 

It’s always kind of fun to see how long it takes me to learn sort of basic things about the technologies I’m using. I think I used SQLite for a web project for the first time in 2022 and I only learned that `ANALYZE` existed today! I imagine in a year or two I’ll be learning about some other very basic feature.

###  some references 

Some blog posts I’ve looked at, other than the official docs:

  * [The definitive guide to using Django with SQLite in production](https://alldjango.com/articles/definitive-guide-to-using-django-sqlite-in-production)
  * [a gist on sqlite performance tuning](https://gist.github.com/phiresky/978d8e204f77feaa0ab5cca08d2d5b27)

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