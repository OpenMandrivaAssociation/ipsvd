Summary:	Internet protocol service daemons
Name:		ipsvd
Version:	1.0.0
Release:	%mkrel 7
License:	BSD
Group:		System/Servers
URL:		http://smarden.org/ipsvd/
Source0:	http://smarden.org/ipsvd/%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
ipsvd is a set of internet protocol service daemons for Unix. It currently
includes a TCP/IP service daemon, and a UDP/IP service daemon. 

An internet protocol service (ipsv) daemon waits for incoming connections on a
local socket; for new connections, it conditionally runs an arbitrary program
with standard input reading from the socket, and standard output writing to the
socket (if connected), to handle the connection. Standard error is used for
logging. 

ipsv daemons can be told to read and follow pre-defined instructions on how to
handle incoming connections; based on the client's IP address or hostname, they
can run different programs, set a different environment, deny a connection, or
set a per host concurrency limit. 

On Linux the network connection optionally can be encrypted using SSLv3. 

Normally the ipsv daemons are run by a supervisor process, such as runsv from
the runit package, or supervise from the daemontools package. 

ipsvd can be used to run services normally run by inetd, xinetd, or tcpserver.

%prep

%setup -q -n net

%build
pushd %{name}-%{version}/src
    make
    make check
popd

%install
rm -rf %{buildroot}

install -d %{buildroot}/sbin/
install -d %{buildroot}%{_mandir}/man{5,7,8}

pushd %{name}-%{version}
    for i in ipsvd-cdb tcpsvd udpsvd; do
	install -m0755 src/$i %{buildroot}/sbin/
    done
popd

install -m0644 %{name}-%{version}/man/*.5 %{buildroot}%{_mandir}/man5/
install -m0644 %{name}-%{version}/man/*.7 %{buildroot}%{_mandir}/man7/
install -m0644 %{name}-%{version}/man/*.8 %{buildroot}%{_mandir}/man8/
rm -f %{buildroot}%{_mandir}/man8/sslio.8*
rm -f %{buildroot}%{_mandir}/man8/sslsvd.8*

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc %{name}-%{version}/package/CHANGES
%doc %{name}-%{version}/package/README
%doc %{name}-%{version}/doc/*.html
%attr(0755,root,root) /sbin/ipsvd-cdb
%attr(0755,root,root) /sbin/tcpsvd
%attr(0755,root,root) /sbin/udpsvd
%attr(0644,root,root) %{_mandir}/man5/ipsvd-instruct.5*
%attr(0644,root,root) %{_mandir}/man7/ipsvd.7*
%attr(0644,root,root) %{_mandir}/man8/ipsvd-cdb.8*
%attr(0644,root,root) %{_mandir}/man8/tcpsvd.8*
%attr(0644,root,root) %{_mandir}/man8/udpsvd.8*


%changelog
* Tue Sep 13 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-7mdv2012.0
+ Revision: 699641
- stop using dietlibc because it's a moving target, too much pain...
- ssl support is no more because it needs matrixssl-1.8.3 (that
  contains security issues), and due to:
  http://permalink.gmane.org/gmane.comp.misc.pape.general/1666
- the mass rebuild of 2010.1 packages

* Tue Feb 02 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-5mdv2010.1
+ Revision: 499591
- rebuild

* Wed Dec 16 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-4mdv2010.1
+ Revision: 479416
- rebuilt against matrixssl-1.8.8

* Sun Aug 23 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-3mdv2010.0
+ Revision: 419986
- rebuilt against matrixssl-1.8.7d

* Thu Sep 11 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-2mdv2009.0
+ Revision: 283679
- rebuilt against latest matrixssl-devel

* Sat Sep 06 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-1mdv2009.0
+ Revision: 282006
- 1.0.0

* Thu Aug 07 2008 Thierry Vignaud <tv@mandriva.org> 0.14.0-4mdv2009.0
+ Revision: 267124
- rebuild early 2009.0 package (before pixel changes)

* Tue Jun 10 2008 Oden Eriksson <oeriksson@mandriva.com> 0.14.0-3mdv2009.0
+ Revision: 217578
- rebuild

* Sun Jun 08 2008 Oden Eriksson <oeriksson@mandriva.com> 0.14.0-2mdv2009.0
+ Revision: 216902
- re-introduce the dietlibc build (requires dietlibc-0.32)

* Tue May 13 2008 Oden Eriksson <oeriksson@mandriva.com> 0.14.0-1mdv2009.0
+ Revision: 206566
- 0.14.0
- don't build it against dietlibc anymore
- rediffed P0

* Wed Jan 02 2008 Olivier Blin <blino@mandriva.org> 0.13.0-2mdv2008.1
+ Revision: 140782
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Wed Sep 05 2007 Oden Eriksson <oeriksson@mandriva.com> 0.13.0-2mdv2008.0
+ Revision: 80457
- build the sslsvd binary as well (whoops!)

* Wed Sep 05 2007 Oden Eriksson <oeriksson@mandriva.com> 0.13.0-1mdv2008.0
+ Revision: 80431
- 0.13.0
- rediffed P0


* Tue Dec 19 2006 Oden Eriksson <oeriksson@mandriva.com> 0.12.1-1mdv2007.0
+ Revision: 100302
- Import ipsvd

* Tue Dec 19 2006 Oden Eriksson <oeriksson@mandriva.com> 0.12.1-1mdv2007.1
- 0.12.1
- rediffed P0

* Sun Feb 05 2006 Oden Eriksson <oeriksson@mandriva.com> 0.12.0-1mdk
- 0.12.0 (Minor feature enhancements)
- rebuilt against matrixssl-1.7.3
- rediff P0

* Thu Oct 20 2005 Oden Eriksson <oeriksson@mandriva.com> 0.11.1-1mdk
- 0.11.1
- rediff P0
- rebuilt against matrixssl-1.7.1

* Wed May 11 2005 Oden Eriksson <oeriksson@mandriva.com> 0.11.0-4mdk
- really rebuilt against matrixssl-1.2.5

* Fri Apr 08 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 0.11.0-3mdk
- rebuilt against matrixssl-1.2.5
- use the %%mkrel macro

* Fri Feb 25 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 0.11.0-2mdk
- rebuilt against matrixssl-1.2.4

* Tue Feb 22 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 0.11.0-1mdk
- 0.11.0
- fix P0

* Tue Jan 18 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 0.10.1-1mdk
- 0.10.1
- fix P0

* Tue Dec 07 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.9.7-1mdk
- 0.9.7
- fix P0

* Thu Aug 05 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.9.6-1mdk
- initial mandrake package

