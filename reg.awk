# Turns the file dump from maint print registers reg.txt to a python array called regs
#
# In gdb
# (gdb) maint print registers reg.txt
# From the shell command line
# in vim, delete the header line and any wierd messages at the end of the list
# $ awk -f reg.awk reg.txt > reg.py
# reg.py was read into aarch64pp.py

BEGIN { 
    printf("regs = ["); 
}

{ 
   if (NR == 1)
       printf "\"%s\"", $1; 
   else
       printf ", \"%s\"", $1; 

   if ((NR % 10) == 0)
       print "";
}

END { 
    print("]"); 
}
