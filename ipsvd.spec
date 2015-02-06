%define _enable_debug_packages %{nil}
%define debug_package %{nil}

Summary:	Internet protocol service daemons
Name:		ipsvd
Version:	1.0.0
Release:	9
License:	BSD
Group:		System/Servers
Url:		http://smarden.org/ipsvd/
Source0:	http://smarden.org/ipsvd/%{name}-%{version}.tar.gz

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

%files
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

#----------------------------------------------------------------------------

%prep
%setup -q -n net

%build
pushd %{name}-%{version}/src
    make
    make check
popd

%install
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

