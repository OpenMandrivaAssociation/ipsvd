%define _enable_debug_packages %{nil}
%define debug_package          %{nil}

Summary:	Internet protocol service daemons
Name:		ipsvd
Version:	0.13.0
Release:	%mkrel 2
License:	BSD
Group:		System/Servers
URL:		http://smarden.org/ipsvd/
Source0:	http://smarden.org/ipsvd/%{name}-%{version}.tar.gz
Patch0:		ipsvd-system_matrixssl.diff
BuildRequires:	dietlibc-devel >= 0.20
BuildRequires:	matrixssl-devel
BuildRoot:	%{_tmppath}/%{name}-buildroot

%description
ipsvd is a set of internet protocol service daemons for Unix. It 
currently includes a TCP/IP service daemon, and a UDP/IP service 
daemon. 

An internet protocol service (ipsv) daemon waits for incoming 
connections on a local socket; for new connections, it conditionally 
runs an arbitrary program with standard input reading from the 
socket, and standard output writing to the socket (if connected), 
to handle the connection. Standard error is used for logging. 

ipsv daemons can be told to read and follow pre-defined instructions 
on how to handle incoming connections; based on the client's IP 
address or hostname, they can run different programs, set a different 
environment, deny a connection, or set a per host concurrency limit. 

On Linux the network connection optionally can be encrypted using 
SSLv3. 

Normally the ipsv daemons are run by a supervisor process, such as 
runsv from the runit package, or supervise from the daemontools 
package. 

ipsvd can be used to run services normally run by inetd, xinetd, or 
tcpserver. 

%prep

%setup -q -n net

pushd %{name}-%{version}/src
%patch0 -p0
popd

%build
# OE: This is quite different from the ordinary to some...
# It makes rpmlint crazy, but what does _it_ know about the real world?
pushd %{name}-%{version}/src
    echo "diet gcc -Os -pipe -nostdinc" > conf-cc
    echo "diet gcc -Os -static -s -nostdinc" > conf-ld
    make
    make sslsvd
#    make check
popd

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

install -d %{buildroot}/sbin/
install -d %{buildroot}%{_mandir}/man{5,7,8}

pushd %{name}-%{version}
    for i in ipsvd-cdb sslio tcpsvd udpsvd sslsvd; do
	install -m0755 src/$i %{buildroot}/sbin/
    done
popd

install -m0644 %{name}-%{version}/man/*.5 %{buildroot}%{_mandir}/man5/
install -m0644 %{name}-%{version}/man/*.7 %{buildroot}%{_mandir}/man7/
install -m0644 %{name}-%{version}/man/*.8 %{buildroot}%{_mandir}/man8/

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc %{name}-%{version}/package/CHANGES
%doc %{name}-%{version}/package/README
%doc %{name}-%{version}/doc/*.html
%attr(0755,root,root) /sbin/ipsvd-cdb
%attr(0755,root,root) /sbin/sslio
%attr(0755,root,root) /sbin/sslsvd
%attr(0755,root,root) /sbin/tcpsvd
%attr(0755,root,root) /sbin/udpsvd
%attr(0644,root,root) %{_mandir}/man5/ipsvd-instruct.5*
%attr(0644,root,root) %{_mandir}/man7/ipsvd.7*
%attr(0644,root,root) %{_mandir}/man8/ipsvd-cdb.8*
%attr(0644,root,root) %{_mandir}/man8/sslio.8*
%attr(0644,root,root) %{_mandir}/man8/sslsvd.8*
%attr(0644,root,root) %{_mandir}/man8/tcpsvd.8*
%attr(0644,root,root) %{_mandir}/man8/udpsvd.8*
