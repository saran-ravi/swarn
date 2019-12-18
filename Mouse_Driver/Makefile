obj-m = m_c.o

#KDIR = /usr/src/linux-headers-4.15.0-70-generic

kv=$(shell uname -r)

all:
	make -C /lib/modules/$(kv)/build M=$(PWD) modules
	#$(MAKE) -C $(KDIR) SUBDIRS=$(PWD) modules

clean:
	make -C /lib/modules/$(kv)/build M=$(PWD) clean
	#rm -rf *.o *.ko *.mod.* *.symvers *.order
