#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
/*
ע��test2.txt��·��
*/
int main()
{
    FILE *fp;
	if ((fp = fopen("test2.txt", "rb")) == NULL) {
		printf("The errno number is%d\n",errno);
		printf("Please check whether the file conforms to the path\n");
		exit(0);
	}
	fseek(fp, 0, SEEK_END);
	int fileLen = ftell(fp);
	char *tmp = (char *)malloc(sizeof(char) * fileLen);
	fseek(fp, 0, SEEK_SET);
	fread(tmp, fileLen, sizeof(char), fp);
	fclose(fp);      //�����ǽ�test.txt�ļ�����������ַ�������ʽд��tmp����ַ���
	//���ļ������������㣬����д�������ø���

    FILE *load;
    if((load=fopen("test3.txt","wb+")) ==NULL){
        printf("The errno number is%d\n",errno);
        exit(0);
    } //��һ���µ��ļ����ȥ��ע�ͺ������


	char *node = tmp;
	int state = 0;
	for (int i = 0; i<fileLen; i++) {
        if (state == 0 && node[i] == '/'){
            state = 1;                      // [xxxxx/]
        }
        else if (state == 1 && node[i] == '*'){
            state = 2;                      // [xxxx/*]
        }
        else if (state == 1 && node[i] == '/'){
            state = 4;                       //[xxxx//]
        }
		else if (state == 1 && node[i] != '/' && node[i] != '*') {
            //putchar('/');                   // ����һ���ʱ��
			putc('/',load);
			state = 0;
		}
        else if (state == 2 && node[i] == '*'){
            state = 3;                      //[xxxx/*xxx*]
        }
        else if (state == 3 && node[i] == '/'){
            state = 0;                      // [xxxx/*xxx*/]
        }
		else if (state == 3 && node[i] != '/'){
			state = 2;                      //[xxxx/*xxx*xxx]
		}
        else if (state == 4 && node[i] == '\\'){
            state = 9;                      //[xxxx//xxxx\\r\n]
        }
        else if (state == 9 && node[i] == '\\'){
            state = 9;                      //[xxxx//xxxx\\\\\\\]
        }
        else if (state == 9 && node[i] != '\n' && node[i] != '\r' && node[i] != ' '){
            state = 4;                      //[xxx//xxxx\xxx\\r\nxxxx]
        }
        else if (state == 4 && node[i] == '\n'){
            state = 0;                      //[xxxx//xxx\r\n]
        }
        else if (state == 0 && node[i] == '\''){
            state = 5;                      //[xxxx']
        }
        else if (state == 5 && node[i] == '\\'){
            state = 6;                         //[xxxx'xxx\\r\n]
        }
        else if (state == 6 && node[i] != '\n' && node[i] != '\r' && node[i] != ' '){
            state = 5;                          //[xxxx'xxx\\r\nxxxx]
        }
        else if (state == 5 && node[i] == '\''){
            state = 0;                      //[xxxx'x/***/x//x']
        }
        else if (state == 0 && node[i] == '\"'){
            state = 7;                      //[xxxx"]
        }
        else if (state == 7 && node[i] == '\\'){
            state = 8;                      //[xxxx"xxx\\r\n]
        }
        else if (state == 8 && node[i] != '\n' && node[i] != '\r' && node[i] != ' '){
            state = 7;                      //[xxx"xxxx\xxx\\r\nxxxx]
        }
        else if (state == 7 && node[i] == '\"'){
            state = 0;                      //[xxx"xxx/**/xx//xx"]
        }


        if ((state == 0 && node[i] != '/') || state == 5 || state == 6 || state == 7 || state == 8)
            putc(node[i],load);             //��ע�͵ģ����ַ�����ĺ����ַ��Ķ�����ӡ���ļ���ȥ
            //putchar(node[i]);
	}
	printf("Success\nPlease open the test3.txt\n");
	exit(1);

}
