Name     : tensorflow-estimator
Version  : 2.3.0
Release  : 84
URL      : https://github.com/tensorflow/estimator/archive/v2.3.0/tensorflow-estimator-2.3.0.tar.gz
Source0  : https://github.com/tensorflow/estimator/archive/v2.3.0/tensorflow-estimator-2.3.0.tar.gz
Summary  : A high-level TensorFlow API
Group    : Development/Tools
License  : Apache-2.0 GPL-3.0 MPL-2.0-no-copyleft-exception
BuildRequires : bazel
BuildRequires : pip
BuildRequires : python3-dev
BuildRequires : setuptools
BuildRequires : six
BuildRequires : tensorflow
BuildRequires : wheel

%define __strip /bin/true
%define debug_package %{nil}

# SOURCES BEGIN
Source10: https://mirror.bazel.build/github.com/bazelbuild/rules_cc/archive/8bd6cd75d03c01bb82561a96d9c1f9f7157b13d0.zip
Source11: https://mirror.bazel.build/github.com/bazelbuild/rules_java/archive/7cf3cefd652008d0a64a419c34c13bdca6c8f178.zip
# SOURCES END

%description
Estimators encapsulate the following actions: training, evaluation, prediction,
export for serving. You may either use the pre-made Estimators we provide or
write your own custom Estimators. All Estimators—whether pre-made or custom—are
classes based on the tf.estimator.Estimator class.

%prep
%setup -q -n estimator-%{version}

InstallCacheBazel() {
  sha256=$(sha256sum $1 | cut -f1 -d" ")
  mkdir -p /var/tmp/cache/content_addressable/sha256/$sha256
  cp $1 /var/tmp/cache/content_addressable/sha256/$sha256/file
}

# CACHE BAZEL BEGIN
InstallCacheBazel %{SOURCE10}
InstallCacheBazel %{SOURCE11}
# CACHE BAZEL END

%build
export http_proxy=http://127.0.0.1:9/
export https_proxy=http://127.0.0.1:9/
export no_proxy=localhost,127.0.0.1,0.0.0.0
export LANG=C.UTF-8
export SOURCE_DATE_EPOCH=1485959355

bazel clean

bazel build \
  --repository_cache=/var/tmp/cache \
  --verbose_failures \
  //tensorflow_estimator/tools/pip_package:build_pip_package

bazel-bin/tensorflow_estimator/tools/pip_package/build_pip_package /var/tmp/estimator_pip

%install
export SOURCE_DATE_EPOCH=1485959355
rm -rf %{buildroot}
pip3 install \
  --no-deps \
  --force-reinstall \
  --ignore-installed \
  --root %{buildroot} \
  /var/tmp/estimator_pip/tensorflow_estimator-%{version}-py2.py3-none-any.whl

%files
%defattr(-,root,root,-)
/usr/lib/python3*/site-packages/tensorflow_estimator*
