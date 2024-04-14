import setuptools

setuptools.setup(
     name="STAcc_v2",
     version="0.1",
     author="Kylyn Smith",
     author_email="kylyn.smith@yale.edu",
     description="A star tracker accuracy package",
     packages=["STAcc_v2","STAcc_v2/object_info", "STAcc_v2/analyze", "STAcc_v2/webapp"]
     python_requires='>=3'
)