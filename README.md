libtdb-1.3.x-srpm
==================

SRPM building tools for libtdb-1.3.x for runing Samba 4 on RHEL 6.

These are built from Fedora rawhide releases, and need to be built and
installed in the following order.

	iniparser-3.1-srpm

	libtalloc-2.1.x-srpm
	libtdb-1.3.x-srpm
	libldb-1.1.x-srpm
	libtevent-0.9.x-srpm

	samba-srpm

The "make" command will do these steps.

	make build	# Build the package on the local OS
	make all	# Use "mock" to build the packages with the local
			# samba4repo-6-x96_64 configuration, which needs.
	make install	# Actually install the RPM's in the designated
			# location for samba4repo-6-x86_64


		Nico Kadel-Garcia <nkadel@gmail.com>
