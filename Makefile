#
# Build mock and local RPM versions of tools for Samba
#

# Assure that sorting is case sensitive
LANG=C

MOCKS+=samba4repo-f35-x86_64
MOCKS+=samba4repo-8-x86_64
MOCKS+=samba4repo-7-x86_64
#MOCKS+=samba4repo-amz2-x86_64

MOCKCFGS+=$(MOCKS)

#REPOBASEDIR=/var/www/linux/samba4repo
REPOBASEDIR:=`/bin/pwd`/../samba4repo

SPEC := `ls *.spec`

all:: $(MOCKS)

.PHONY: getsrc
getsrc::
	spectool -g $(SPEC)

srpm:: src.rpm

#.PHONY:: src.rpm
src.rpm:: Makefile
	@rm -rf rpmbuild
	@rm -f $@
	@echo "Building SRPM with $(SPEC)"
	rpmbuild --define '_topdir $(PWD)/rpmbuild' \
		--define '_sourcedir $(PWD)' \
		-bs $(SPEC) --nodeps
	mv rpmbuild/SRPMS/*.src.rpm src.rpm

.PHONY: build
build:: src.rpm
	rpmbuild --define '_topdir $(PWD)/rpmbuild' \
		--rebuild $?

.PHONY: $(MOCKS)
$(MOCKS):: src.rpm
	@if [ -e $@ -a -n "`find $@ -name \*.rpm 2>/dev/null`" ]; then \
		echo "	Skipping RPM populated $@"; \
	else \
		echo "Actally building $? in $@"; \
		rm -rf $@; \
		mock -q -r $(PWD)/../$@.cfg \
		     --resultdir=$(PWD)/$@ \
		     $?; \
	fi

mock:: $(MOCKS)

install:: $(MOCKS)
	@for repo in $(MOCKS); do \
	    echo Installing $$repo; \
	    case $$repo in \
		amazonlinux-2-x86_64) yumrelease=amzn/2; yumarch=x86_64; ;; \
		*-amz2-x86_64) yumrelease=amazon/2; yumarch=x86_64; ;; \
		*-7-x86_64) yumrelease=el/7; yumarch=x86_64; ;; \
		*-8-x86_64) yumrelease=el/8; yumarch=x86_64; ;; \
		*-35-x86_64) yumrelease=fedora/35; yumarch=x86_64; ;; \
		*-f35-x86_64) yumrelease=fedora/35; yumarch=x86_64; ;; \
		*-rawhide-x86_64) yumrelease=fedora/rawhide; yumarch=x86_64; ;; \
		*) echo "Unrecognized release for $$repo, exiting" >&2; exit 1; ;; \
	    esac; \
	    rpmdir=$(REPOBASEDIR)/$$yumrelease/$$yumarch; \
	    srpmdir=$(REPOBASEDIR)/$$yumrelease/SRPMS; \
	    echo "Pushing SRPMS to $$srpmdir"; \
	    rsync -av $$repo/*.src.rpm --no-owner --no-group $$repo/*.src.rpm $$srpmdir/. || exit 1; \
	    createrepo_c -q $$srpmdir/.; \
	    echo "Pushing RPMS to $$rpmdir"; \
	    rsync -av $$repo/*.rpm --exclude=*.src.rpm --exclude=*debuginfo*.rpm --no-owner --no-group $$repo/*.rpm $$rpmdir/. || exit 1; \
	    createrepo_c -q $$rpmdir/.; \
	done
	@for repo in $(MOCKCFGS); do \
	    echo "Touching $(PWD)/../$$repo.cfg"; \
	    /bin/touch --no-dereference $(PWD)/../$$repo.cfg; \
	done

clean::
	rm -rf */
	rm -f *.out
	rm -f *.rpm

realclean distclean:: clean
