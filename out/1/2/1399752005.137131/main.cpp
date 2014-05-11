#include <iostream>
#include <cstdlib>
#include <vector>
#include "cv.h"
#include "ml.h"
#include "highgui.h"
#include "dataset.h"
#include "feature.h"
#include <ctime>
using namespace std;
using namespace cv;

#define TESTSETSIZE 100
#define TRAINSETSIZE 100

#define MAXFVSIZE 200000000/4 //1000000 bytes div by 4 bytes per one float number




void make_simple(vector<Rect> &rects){
  //remove inner rects
  for (int i=rects.size()-1;i>-1;i--){
	for (int l=0;l<i;l++){
	  if( rects[l].x>=rects[i].x && 
		  rects[l].x+rects[l].width<=rects[i].x+rects[i].width &&
		  rects[l].y>=rects[i].y && 
		  rects[l].y+rects[l].height<=rects[i].y+rects[i].height
		  ){
		rects.erase(rects.begin()+l);
		break;
	  }

	}
  }
  //join rects
  for (int i=rects.size()-1;i>-1;i--){
	for (int l=0;l<i;l++){
	  if(( rects[i].x==rects[l].x &&
		  rects[i].width ==rects[l].width )
		 ||
		 (rects[i].y==rects[l].y &&
		  rects[i].height ==rects[l].height)
		 ){
		rects[i] = rects[i]|rects[l];
		rects.erase(rects.begin()+l);
		break;
	  }

	}
  }
  
}






int main(int argc, char** argv) {
  time_t t,old_t;
  old_t=t = time(0);
  cout << "Timestamp: " << t<<endl;
  DataSet *dataset = new ICDAR2011DataSet(TRAINSETSIZE);

//  Mat im = *dataset->getBadImg();
//   int i = 1000;
//   while( i){
//    namedWindow("Image",CV_WINDOW_AUTOSIZE);
//    imshow("Image",im);
//    waitKey(100);
//    im = *dataset->getBadImg();
//    i--;
//  }

  Features features1,features2,features3;
//  features1.add_feature(&FSTD);
  features1.add_feature(&FGradHist);

//  features1.add_feature(&FXDerivative);
//  features1.add_feature(&FYDerivative);

  features2.add_feature(&FGradSTD);
//  features2.add_feature(&FEntropyGrey);
  //features2.add_feature(&FIntHist);
  //features2.add_feature(&FIntGradHist);
 features2.add_feature(&SWTDumb);

 features3.add_feature(&FHolland);

  //ntestsamples > 10, otherwise boosting does not work?
  int goodtrainsamples = 0; 
  Mat* img;
  img=  dataset->getGoodImg();


  //---------------------------------------------------------------------------
  //==========================================================================
  //===                                                                    ===
  //===                                                                    ===
  //===                                                                    ===
  //===                  FIRST CASCADE                                     ===
  //===                                                                    ===
  //===                                                                    ===
  //===                                                                    ===
  //==========================================================================
  //---------------------------------------------------------------------------

  //---------------------------------------------------------------------------
  //generating feature vector
  //---------------------------------------------------------------------------

  Mat* featureVector = new Mat(0,features1.num_of_features(),CV_32FC1);// = features.generate_feature_vector(image);
  //Mat classLabelResponses(0, 1, CV_32FC1);;//(nsamples_all, 1, CV_32F);
  int imgn = 0;

   while(img->data){
   	imgn++;
   	cout << "image piece number: "<< imgn << endl;
	bool width = true;
	int s = 0;
	if (img->cols > img->rows){
	  s = img->rows;
	  width = true;
	}	else{
	  s= img->cols;
	  width = false;
	}
	int x = 0,y=0;
	
	if (width){
	  while(x+s<img->cols){
		  Rect current(x,y,s,s);
		  Mat subimg = Mat(*img,current);
		  featureVector->push_back(features1.generate_feature_vector(subimg));
		  goodtrainsamples++;
		  x+=s/3;
	  } 
	}else{
	  while(y+s<img->rows){
		  Rect current(x,y,s,s);
		  Mat subimg = Mat(*img,current);
		  featureVector->push_back(features1.generate_feature_vector(subimg));
		  goodtrainsamples++;
		  y+=s/3;
	  }
	}
	  
   	delete img;
   	img = dataset->getGoodImg();
   }
   delete img;  


   for (int i = 0; i<goodtrainsamples; i++){
   	img = dataset->getBadImg();
   	featureVector->push_back(features1.generate_feature_vector(*img));
   	delete img;
   }
   //delete img;

   Mat classLabelResponses(featureVector->rows, 1, CV_32FC1,-1.0f);
   Mat goodroi = classLabelResponses(Range(0,goodtrainsamples),Range::all());
   goodroi = Scalar(1.0f);
   Mat badroi = classLabelResponses(Range(goodtrainsamples,classLabelResponses.rows),Range::all());
   badroi = Scalar(-1.0f);

   // number of single features=variables 
   int var_count = featureVector->cols; 
   // number of samples=feature vectors
   int nsamples_all = featureVector->rows; 
   //cout << featureVector << endl;
   //cout << classLabelResponses << endl;
   printf("data dim1: %d rows, %d columns /nresponses dim: %d rows, %d columns\n", 
   		 featureVector->rows, 
   		 featureVector->cols, 
   		 classLabelResponses.rows, 
   		 classLabelResponses.cols);
  

   Mat var_type(var_count+1,1,CV_8UC1,1);
   
   Mat end = var_type(Range(0,var_type.rows-1),Range::all());
   end = Scalar(CV_VAR_NUMERICAL  );
   //   var_type.at<bool>(var_count,0) = CV_VAR_CATEGORICAL;

   printf("var_type dim: %d rows, %d columns\n", 
   		 var_type.rows, var_type.cols);
   cout << var_type << endl;
   cout << classLabelResponses << endl;

   t = time(0)-old_t;
   old_t = time(0);
   cout << "Time: " << t<<endl;

   //-------------------------------------------------------------------------
   //TRAINING
   //------------------------------------------------------------------------  


   printf("Training ... ");
   float priors[]={1.0f,10.0f}; // to get more false positives
   CvBoost boost1; 
   Mat voidmat;
   cout << boost1.train(
   			  *featureVector, CV_ROW_SAMPLE, 
   			  classLabelResponses,voidmat,voidmat,
			  var_type,
			  voidmat,
			  CvBoostParams(CvBoost::REAL, 100,0.95,1,true,priors));//, 

   printf("done!\n");

   // saving training results
   boost1.save("./boost1cascade.xml", "boost");

   t = time(0)-old_t;
   old_t = time(0);
   cout << "Time train 1: " << t<<endl; 

   //---------------------------------------------------------------------------
   //==========================================================================
   //===                                                                    ===
   //===                                                                    ===
   //===                                                                    ===
   //===                  SECOND CASCADE                                    ===
   //===                                                                    ===
   //===                                                                    ===
   //===                                                                    ===
   //==========================================================================
   //---------------------------------------------------------------------------

   //---------------------------------------------------------------------------
   //generating feature vector
   //---------------------------------------------------------------------------
   //featureVector.release();
   delete featureVector;
   featureVector = new Mat(0,features2.num_of_features(),CV_32FC1);
   //classLabelResponses.release();
   classLabelResponses = Mat(0,1,CV_32FC1);

   delete dataset;
   dataset = new ICDAR2011DataSet(TRAINSETSIZE);
   cout << endl << "SECOND CASCADE" << endl;

   img = dataset->getfoolgoodimg();
    imgn=0;

   bool enough = false;
 
   ulong  max_fv_size = MAXFVSIZE/ features2.num_of_features();
   cout<< MAXFVSIZE  << "   ;ajsdf;  "<< max_fv_size <<endl;
   ulong  currentNci = 0;
   while(img->data && !enough){
     int x = 0,y=0;
     int s = 20;
     cout << "image number: "<<imgn<<endl;

     while(s < img->cols/5 && s < img->rows/5 && !enough){
       while(y+s<img->rows && !enough){
         while(x+s<img->cols && !enough){
           Rect current(x,y,s,s);
           Mat subimg = Mat(*img, current);
           if (boost1.predict(features1.generate_feature_vector(subimg))>0)
             {
               try {
                 if (currentNci < max_fv_size){
                   featureVector->push_back(features2.generate_feature_vector(subimg));
                   classLabelResponses.push_back(dataset->is_good_rect(current,0.9));
                 }else{
                   if (rand()*1.0/RAND_MAX*1.0 < max_fv_size*1.0/currentNci){
                     int row_num = rand()%featureVector->rows;
                     features2.generate_feature_vector(subimg).row(0).copyTo(featureVector->row(row_num));
                     classLabelResponses.at<float>(row_num) = dataset->is_good_rect(current,0.9);
                   }
                 }
                 currentNci ++;
                 if (currentNci < 10) cout << "+";
               }
               catch(cv::Exception){
                 enough = true;
                 break;
               }
             }
           x+=s/3;
         }
         x = 0;
         y += s/3;
       }
       y = 0;
       x=0;
       s =ceil(s*1.2);
     }
     delete(img);
     img = dataset->getfoolgoodimg();
     imgn++;
    }//while{img.data}
    delete(img);
	cout << "DEBUG:   "<< currentNci<< endl;

   // number of single features=variables 
   var_count = featureVector->cols; 
   // number of samples=feature vectors
   nsamples_all = featureVector->rows; 
   //cout << featureVector << endl;
   //cout << classLabelResponses << endl;
   printf("data dim2: %d rows, %d columns /nresponses dim: %d rows, %d columns\n", 
   		 featureVector->rows, 
   		 featureVector->cols, 
   		 classLabelResponses.rows, 
   		 classLabelResponses.cols);
  
   var_type.release();
   var_type = Mat(var_count+1,1,CV_8UC1,1);
   end = var_type(Range(0,var_type.rows-1),Range::all());
   end = Scalar(CV_VAR_NUMERICAL  );
   //   var_type.at<bool>(var_count,0) = CV_VAR_CATEGORICAL;

   printf("var_type dim: %d rows, %d columns\n", 
   		 var_type.rows, var_type.cols);
   cout << var_type << endl;
   //cout << classLabelResponses << endl;

   t = time(0)-old_t;
   old_t = time(0);
   cout << "Time: " << t<<endl;

   //-------------------------------------------------------------------------
   //TRAINING
   //------------------------------------------------------------------------  

   printf("Training ... ");
   CvBoost boost2; 
   boost2.clear();
   float priors2[]={1.0f,5.0f}; // to get more false positives
   cout << boost2.train(
						*featureVector, 
						CV_ROW_SAMPLE, 
						classLabelResponses,
						voidmat,voidmat,
						var_type,
						voidmat,
						CvBoostParams(CvBoost::REAL, 100,0.95,1,true,priors2));//, 

   printf("done!\n");

   // saving training results
   boost2.save("./boost2cascade.xml", "boost");

   t = time(0)-old_t;
   old_t = time(0);
   cout << "Time train 2: " << t<<endl; 
   //---------------------------------------------------------------------------
   //==========================================================================
   //===                                                                    ===
   //===                                                                    ===
   //===                                                                    ===
   //===                  THIRD CASCADE                                     ===
   //===                                                                    ===
   //===                                                                    ===
   //===                                                                    ===
   //==========================================================================
   //---------------------------------------------------------------------------

   //---------------------------------------------------------------------------
   //generating feature vector
   //---------------------------------------------------------------------------
   //featureVector.release();
   delete featureVector;
   featureVector = new Mat(0,features2.num_of_features(),CV_32FC1);
   //classLabelResponses.release();
   classLabelResponses = Mat(0,1,CV_32FC1);

   delete dataset;
   dataset = new ICDAR2011DataSet(TRAINSETSIZE);
   cout << endl << "THIRD CASCADE" << endl;

   img = dataset->getfoolgoodimg();
   imgn = 0 ;

   enough = false;
 
   max_fv_size = MAXFVSIZE/ features3.num_of_features();
   cout<< MAXFVSIZE  << "   ;ajsdf;  "<< max_fv_size <<endl;
   currentNci = 0;

   while(img->data && !enough){
     int x = 0,y=0;
     int s = 20;
     cout << "image number: "<<imgn<<endl;

     while(s < img->cols/5 && s < img->rows/5 && !enough && featureVector->rows < 500000){
       while(y+s<img->rows && !enough){
         while(x+s<img->cols && !enough){
           Rect current(x,y,s,s);
           Mat subimg = Mat(*img, current);
           if (boost1.predict(features1.generate_feature_vector(subimg))>0)
             {
               if (boost2.predict(features2.generate_feature_vector(subimg))>0)
                 {
                   try {
                     if (currentNci < max_fv_size){
                       featureVector->push_back(features3.generate_feature_vector(subimg));
                       classLabelResponses.push_back(dataset->is_good_rect(current,0.9));
                     }else{
                       if (rand()*1.0/RAND_MAX*1.0 < max_fv_size*1.0/currentNci){
                         int row_num = rand()%featureVector->rows;
                         features3.generate_feature_vector(subimg).row(0).copyTo(featureVector->row(row_num));
                         classLabelResponses.at<float>(row_num) = dataset->is_good_rect(current,0.9);
                       }
                     }
                     currentNci ++;
                     if (currentNci < 10) cout << "+";
                   }
                   catch(cv::Exception){
                     enough = true;
                     break;
                   }
                 }
             }
           x+=s/3;
         }
         x = 0;
         y += s/3;
       }
       y = 0;
       x=0;
       s =ceil(s*1.2);
     }
     delete(img);
     img = dataset->getfoolgoodimg();
     imgn++;
    }//while{img.data}
    delete(img);
    cout << "DEBUG:   "<< currentNci<< endl;

	

   // number of single features=variables 
   var_count = featureVector->cols; 
   // number of samples=feature vectors
   nsamples_all = featureVector->rows; 
   //cout << featureVector << endl;
   //cout << classLabelResponses << endl;
   printf("data dim3: %d rows, %d columns /nresponses dim: %d rows, %d columns\n", 
   		 featureVector->rows, 
   		 featureVector->cols, 
   		 classLabelResponses.rows, 
   		 classLabelResponses.cols);
  
   var_type.release();
   var_type = Mat(var_count+1,1,CV_8UC1,1);
   end = var_type(Range(0,var_type.rows-1),Range::all());
   end = Scalar(CV_VAR_NUMERICAL  );
   //   var_type.at<bool>(var_count,0) = CV_VAR_CATEGORICAL;

   printf("var_type dim: %d rows, %d columns\n", 
   		 var_type.rows, var_type.cols);
   cout << var_type << endl;
   //cout << classLabelResponses << endl;

   t = time(0)-old_t;
   old_t = time(0);
   cout << "Time: " << t<<endl;

   //-------------------------------------------------------------------------
   //TRAINING
   //------------------------------------------------------------------------  

   printf("Training ... ");
   CvBoost boost3; 
   boost3.clear();
   float priors3[]={1.0f,1.0f}; // to get more false positives
   cout << boost3.train(
						featureVector->operator()(Range(0,classLabelResponses.rows),Range::all()), 
						CV_ROW_SAMPLE, 
						classLabelResponses,
						voidmat,voidmat,
						var_type,
						voidmat,
						CvBoostParams(CvBoost::REAL, 100,0.95,1,true,priors3));//, 

   printf("done!\n");

   // saving training results
   boost3.save("./boost3cascade.xml", "boost");

   t = time(0)-old_t;
   old_t = time(0);
   cout << "Time train 3: " << t<<endl; 
   
   delete featureVector;
   
   //-------------------------------------------------------------------------
   //BOOTSTRAPING
   //-------------------------------------------------------------------------
#ifdef bootstrap
   delete dataset;
   dataset = new ICDAR2011DataSet(TRAINSETSIZE);
   cout << endl << "BOOTSTRAPING" << endl;

   img = dataset->getfoolgoodimg();
   imgn = 0 ;

   while(img->data){
   	 Mat fvector;//(0,features.num_of_features(),CV_32FC1);
   	 Mat clResp(0,1,CV_32FC1);
   	 int x = 0,y=0;
   	 int s = 20;
	 cout << "image number: "<<imgn<<endl;



   	 cout << img->rows<<" " << img->cols << endl;
   	 while(s < img->cols/5 && s < img->rows/5){
   	   while(y+s<img->rows){
   		 while(x+s<img->cols){
   		   Rect current(x,y,s,s);
		   Mat subimg = Mat(*img, current);
		   Mat feature = Mat(1,459,CV_32FC1,1);//features.generate_feature_vector(subimg);
		   float p_good = boost.predict(feature);
		   
   		   if (dataset->is_good_rect(current,0.9)){
			 if (p_good<0){
			   clResp.push_back(1.0f);
			   fvector.push_back(feature);
			 }
   		   }else{
			 if (p_good>0){
			   fvector.push_back(feature);
			   clResp.push_back(-1.0f);
			 }
   		   }
		  
   		   x+=s/3;
   		 }
   		 x = 0;
   		 y += s/3;
   	   }
   	   y = 0;
   	   x=0;
   	   s =ceil(s*1.2);
   	 }//whiel(s < img.cols/5)
   	 //cout << "size for features: "<<featureVector.size();
	 printf("data dim: %d rows, %d columns /nresponses dim: %d rows, %d columns\n", 
			fvector.rows, 
			fvector.cols, 
			clResp.rows, 
			clResp.cols);
	 
   	 //cout << fvector << endl;
   	 //cout << clResp << endl;
   	 cout << "not bad before";
	 boost.train(
   	  			 fvector, CV_ROW_SAMPLE, 
   	  			 clResp,Mat(),Mat(),Mat(),Mat(),
				 boost.get_params(),
	  			 true);//update = true 
	 cout << "not bad after";	 
	 
   	 delete(img);
   	 img = dataset->getfoolgoodimg();
   	 imgn++;
    }//while{img.data}
    delete(img);

   // saving bootstrping results
   boost.save("./boosttest_allnighter_after.xml", "boost");

   t = time(0)-old_t;
   old_t = time(0);
   cout << "Time: " << t<<endl; 
#endif
   //--------------------------------------------------------------------------
   //TESTING
   //-------------------------------------------------------------------------
   dataset = new ICDAR2011TestDataSet(100-TESTSETSIZE);
   cout << endl<< endl<<"REAL TESTING"<<endl;

	img = dataset->getTesting();

	double total_r=0;
	double total_p=0;
	int    total_c=0;
	imgn = 0;
	while(img->data){
	  cout << "image number: "<< imgn++<<endl;
	  int x = 0,y=0;
	  int s = 20;
	  int layers = 0;
	  vector<Rect> positives;
	  while(s < img->cols/5 && s < img->rows/5){
		while(y+s<img->rows){
		  while(x+s<img->cols){
			Rect current(x,y,s,s);
			//cout << "Debug: r " << img.rows<< " c "<<img.cols<<" R "<<current<<endl;
			if (boost1.predict(features1.generate_feature_vector(img->operator()(current)))>0){
			  if (boost2.predict(features2.generate_feature_vector(img->operator()(current)))>0){
				if (boost3.predict(features3.generate_feature_vector(img->operator()(current)))>0)
				  positives.push_back(current);
			  }
			}
			x+=s/3;
		  }
		  //we dont want to loose most right pixels
		  Rect current(img->cols-s-1,y,s,s);
		  //cout << "Debug: r " << img.rows<< " c "<<img.cols<<" R "<<current<<endl;
		  if (boost1.predict(features1.generate_feature_vector(img->operator()(current)))>0){
			positives.push_back(current);
		  }
		  x=0;
		  y+=s/3;
		}
		//and the bottom ones
		y = img->rows - s -1;
		while(x+s<img->cols){
		  Rect current(x,y,s,s);
		  //cout << "Debug: r " << img.rows<< " c "<<img.cols<<" R "<<current<<endl;
		  if (boost1.predict(features1.generate_feature_vector(img->operator()(current)))>0){
			positives.push_back(current);
		  }
		  x+=s/3;
		}
		Rect current(img->cols-s-1,y,s,s);
		//cout << "Debug: r " << img.rows<< " c "<<img.cols<<" R "<<current<<endl;
		if (boost1.predict(features1.generate_feature_vector(img->operator()(current)))>0){
		  positives.push_back(current);
		}
		y = 0;
		x=0;
		s =ceil(s*1.2);
		layers++;
	  }//whiel(s < img.cols/5)


	  vector<Rect> old_p = positives; 
	  make_simple(positives);
	  do{
		  old_p = positives;
		  make_simple(positives);
	  }while(old_p.size() != positives.size());
	
	  double p,r,f;
	  f = dataset->check(positives,p,r);
	  
	  // cout << "f measure: "<< f<< endl;
	  // cout << "Precision: "<< p<< endl;
	  // cout << "Recall   : "<< r<< endl;

	  total_p+=p;
	  total_r+=r;
	  total_c++;
	  
	  // cout << total_c<<endl;
	  
	  
	  delete img;
	  img = dataset->getTesting();
	}//while{img.data}
	delete img ;

	t = time(0)-old_t;
	old_t = time(0);
	cout << "Time: " << t<<endl;
	total_p /= total_c;
	total_r /= total_c;
	double total_f = 1/(0.5/total_p + 0.5/total_r);
	cout <<"TOTAL SCORE"<< endl;
	cout << "f measure: "<< total_f<< endl;
	cout << "Precision: "<< total_p<< endl;
	cout << "Recall   : "<< total_r<< endl;
	

	//making image
	delete	dataset;
	dataset = new ICDAR2011TestDataSet(30);

	img = dataset->getTesting();
	{
	  int x = 0,y=0;
	  int s = 20;
	  int layers = 0;
	  vector<Rect> positives;
	  while(s < img->cols/5 && s < img->rows/5){
		while(y+s<img->rows){
		  while(x+s<img->cols){
			Rect current(x,y,s,s);
			//cout << "Debug: r " << img.rows<< " c "<<img.cols<<" R "<<current<<endl;
			if (boost1.predict(features1.generate_feature_vector(img->operator()(current)))>0){
			  if (boost2.predict(features2.generate_feature_vector(img->operator()(current)))>0){
				if (boost3.predict(features3.generate_feature_vector(img->operator()(current)))>0)
				  positives.push_back(current);
			  }
			}
			x+=s/3;
		  }
		  //we dont want to loose most right pixels
		  Rect current(img->cols-s-1,y,s,s);
		  //cout << "Debug: r " << img.rows<< " c "<<img.cols<<" R "<<current<<endl;
		  if (boost1.predict(features1.generate_feature_vector(img->operator()(current)))>0){
			positives.push_back(current);
		  }
		  x=0;
		  y+=s/3;
		}
		//and the bottom ones
		y = img->rows - s -1;
		while(x+s<img->cols){
		  Rect current(x,y,s,s);
		  //cout << "Debug: r " << img.rows<< " c "<<img.cols<<" R "<<current<<endl;
		  if (boost1.predict(features1.generate_feature_vector(img->operator()(current)))>0){
			positives.push_back(current);
		  }
		  x+=s/3;
		}
		Rect current(img->cols-s-1,y,s,s);
		//cout << "Debug: r " << img.rows<< " c "<<img.cols<<" R "<<current<<endl;
		if (boost1.predict(features1.generate_feature_vector(img->operator()(current)))>0){
		  positives.push_back(current);
		}
		y = 0;
		x=0;
		s =ceil(s*1.2);
		layers++;
	  }//whiel(s < img.cols/5)
	  
	   Mat dst;
	   cvtColor(*img,dst,CV_RGB2RGBA);

	   Mat dstd;
	   for (int i=0;i<positives.size();i++)
	   {
		 Mat mask(dst.rows,dst.cols,dst.type());

		 rectangle(mask,positives[i],Scalar(0,0,200,100),-1);
		 add(mask,dst,dstd);
		 dstd.copyTo(dst);
	   }

	   char filename[25];
	   time_t now = time(NULL);
	   strftime(filename, 20, "%Y%m%d%H%M%S.png", localtime(&now));
	   cout << filename << endl;
	   // Mat dstd;
	   imwrite(filename,dstd);
	}
	delete img ;





	return EXIT_SUCCESS;
	
}






