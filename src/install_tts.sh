pwd
git clone https://github.com/jaywalnut310/vits.git
python --version
cd vits/

pip install Cython==0.29.21
pip install librosa==0.8.0
pip install phonemizer==2.2.1
pip install scipy
pip install numpy
pip install torch
pip install torchvision
pip install matplotlib
pip install Unidecode==1.1.1

cd monotonic_align/
mkdir monotonic_align
python3 setup.py build_ext
cd ../
pwd
