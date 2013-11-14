
#include <Python.h>
#include <numpy/arrayobject.h>
#include <stdbool.h>

        
static PyObject* Lee2(PyObject* self, PyObject* args)
{
    PyArrayObject *array, *start, *bonus,*out;
    if (!PyArg_ParseTuple(args, "O!O!O!O!",&PyArray_Type, &array,&PyArray_Type, &start,&PyArray_Type, &bonus,&PyArray_Type, &out))
        return NULL;
    if (array->nd != 2) {
        PyErr_SetString(PyExc_ValueError,"array must be two-dimensional.");
        return NULL;
    }
    if (array->descr->type_num != PyArray_LONG) {
        PyErr_SetString(PyExc_ValueError,"array must be of type int.");
        return NULL;
    }
    

    
    int *Cstart;
    Cstart = (int*) malloc(2*sizeof(int*));
    Cstart[0] = (start->data)[0];
    int s = *(int*)(start->data + start->strides[0] );
    Cstart[1] = s;
    
    int i,j;
    
    int bn = bonus->dimensions[0];
    int **Cbonus;
    Cbonus = (int**) malloc(bn*sizeof(int*));
    for (i = 0; i < bn; i++) {
        Cbonus[i] = (int*) malloc(2*sizeof(int));
        for (j = 0; j < 2; j++) {
            int s = *(int*)(bonus->data + i*bonus->strides[0] + j*bonus->strides[1]);
            Cbonus[i][j] = s;
        }
    }
    //============================================
    int n,m;
    n = array->dimensions[0];
    m = array->dimensions[1];
    bool **mask;
    int **labels;
    mask = (bool**) malloc(m*sizeof(bool*));
    labels = (int**) malloc(m*sizeof(int*));
    for (i = 0; i < m; i++) {
        mask[i] = (bool*) malloc(n*sizeof(bool)); 
        labels[i] = (int*) malloc(n*sizeof(int)); 
    }
    //============================================
    int y,x;    
    for (y = 0; y < n; y++){
        for (x = 0; x < m; x++){
            mask[x][y] = false;
            labels[x][y] = -1;
        }
    }
    
    //============================================

    labels[Cstart[1]][Cstart[0]] = 0;
    
    bool hasConv = true;
    while(hasConv ){
        int cc=0;
        
        hasConv = false;
        for (y = 0; y < n; y++){
            for (x = 0; x < m; x++){
                int l = labels[x][y];
                
                if(!mask[x][y] && labels[x][y] >-1){ //has not been used
                    
                    int s = *(int*)(array->data + y*array->strides[0] + x*array->strides[1]);
                    int s_up=1,s_right=1,s_down=1,s_left=1;
                    int l_up=-1,l_right=-1,l_down=-1,l_left=-1;
                    
                    if(x>0){
                        if(!mask[x-1][y]){
                            s_left = *(int*)(array->data + y*array->strides[0] + (x-1)*array->strides[1]);
                            if(!s_left){
                                labels[x-1][y] = l+s_left+1;
                                mask[x][y]=true;
                                hasConv = true;
                            }
                        }
                    }
                    if(x<(m-1)){
                        if(!mask[x+1][y]){
                            s_right = *(int*)(array->data + y*array->strides[0] + (x+1)*array->strides[1]);
                            //~ 
                            if(!s_right){
                                labels[x+1][y] = l+1;
                                mask[x][y]=true;
                                hasConv = true;
                            }
                        }
                    }
                    if(y>0){
                        if(!mask[x][y-1]){
                            s_up = *(int*)(array->data + (y-1)*array->strides[0] + x*array->strides[1]);
                            if(!s_up){
                                labels[x][y-1] = l+1;
                                mask[x][y]=true;
                                hasConv = true;
                            }
                        }
                    }
                    
                    if(y<(n-1)){
                        if(!mask[x][y+1]){
                            s_down = *(int*)(array->data + (y+1)*array->strides[0] + x*array->strides[1]);
                            if(!s_down){
                                labels[x][y+1] = l+1;
                                mask[x][y]=true;
                                hasConv = true;
                            }
                        }
                    }
                }
            }
        }
        
    }
    
    for (i = 0; i < n; i++) {
        for (j = 0; j < m; j++) {
           *(long*)(out->data + i*out->strides[0] + j*out->strides[1]) = labels[j][i];            
        }
    }
    
    for (i = 0; i < m; i++) {
       free(mask[i]);  
       free(labels[i]);  
    }
    
    for (i = 0; i < bn; i++) {
       free(Cbonus[i]);  
    }
    
    free(mask);  
    free(labels);  
    free(Cbonus);  
    free(Cstart); 
    Py_RETURN_NONE;
}
 
 
 
 
 
 
static PyMethodDef AIMethods[] =
{
     {"Lee2", Lee2, METH_VARARGS, "???"},
     {NULL, NULL, 0, NULL}
};
 
PyMODINIT_FUNC
 
initC_AI(void)
{
     (void) Py_InitModule("C_AI", AIMethods);
     import_array();
}
