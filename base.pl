 #!/usr/bin/env perl
 use Mojo::Webqq;
 my ($host,$port,$post_api);
 
 $host = "0.0.0.0"; #������Ϣ�ӿڼ�����ַ��û��������Ҫ�벻Ҫ�޸�
 $port = 5000;      #������Ϣ�ӿڼ����˿ڣ��޸�Ϊ�Լ�ϣ�������Ķ˿�
 #$post_api = 'http://xxxx';  #���յ�����Ϣ�ϱ��ӿڣ��������Ҫ������Ϣ�ϱ�������ɾ����ע�ʹ���
 
 my $client = Mojo::Webqq->new();
 $client->load("ShowMsg");
 $client->load("Openqq",data=>{listen=>[{host=>$host,port=>$port}], post_api=>$post_api});
 $client->run();