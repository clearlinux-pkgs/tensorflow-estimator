Name     : tensorflow-estimator
Version  : 1.15.1
Release  : 77
URL      : https://github.com/tensorflow/estimator/archive/v1.15.1.tar.gz
Source0  : https://github.com/tensorflow/estimator/archive/v1.15.1.tar.gz
Source1 : https://github.com/bazelbuild/rules_pkg/releases/download/0.2.0/rules_pkg-0.2.0.tar.gz
Source2 : https://github.com/bazelbuild/rules_cc/archive/0d5f3f2768c6ca2faca0079a997a97ce22997a0c.zip
Source3 : https://github.com/bazelbuild/rules_proto/archive/b0cc14be5da05168b01db282fe93bdf17aa2b9f4.tar.gz

%define __strip /bin/true
%define debug_package %{nil}


#Source104: 0001-enum34-is-only-required-for-Python-3.4.patch

Summary  : No detailed summary available
Group    : Development/Tools
License  : Apache-2.0 GPL-3.0 MPL-2.0-no-copyleft-exception
BuildRequires : pip

BuildRequires : python3-dev
BuildRequires : setuptools
BuildRequires : wheel
BuildRequires : openjdk
BuildRequires : openjdk-dev
BuildRequires : numpy
#BuildRequires : six
#BuildRequires : protobuf
#BuildRequires : protobuf-c
BuildRequires : bazel
BuildRequires : Keras
BuildRequires : Keras_Applications
BuildRequires : Keras_Preprocessing
BuildRequires : mkl-dnn-dev
BuildRequires : c-ares-dev
BuildRequires : tensorflow
BuildRequires : wrapt




Requires: Werkzeug
Requires: Markdown
Requires: bleach
Requires: backports.weakref
Requires: tensorboard
Requires: absl-py
Requires: astor
Requires: grpcio
Requires: gast
Requires : Keras
Requires : Keras_Applications
Requires : Keras_Preprocessing
Requires : termcolor


%description
TensorFlow

%prep
%setup -q  -n estimator-1.15.1

#%patch2 -p1

%build
export LANG=C
export SOURCE_DATE_EPOCH=1485959355

InstallCache() {
	sha256=`sha256sum $1 | cut -f1 -d" "`
	mkdir -p /tmp/cache/content_addressable/sha256/$sha256/
	cp $1 /tmp/cache/content_addressable/sha256/$sha256/file
}

InstallCache %{SOURCE1}
InstallCache %{SOURCE2}
InstallCache %{SOURCE3}

bazel clean
bazel build --repository_cache=/tmp/cache //tensorflow_estimator/tools/pip_package:build_pip_package
bazel-bin/tensorflow_estimator/tools/pip_package/build_pip_package /tmp/estimator_pip


%install
export SOURCE_DATE_EPOCH=1485959355


pip3 install --no-deps --force-reinstall --root %{buildroot}  /tmp/estimator_pip/tensorflow_estimator-1.15.1-py2.py3-none-any.whl

%files
%defattr(-,root,root,-)
/usr/lib/python3.7/site-packages/tensorflow_estimator*
